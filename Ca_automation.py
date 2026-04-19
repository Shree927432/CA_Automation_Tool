import os
import smtplib
from email.message import EmailMessage

import pandas as pd
from dotenv import load_dotenv


PORTAL_FILE = "portal_data.csv"
CLIENT_FILE = "client_data.csv"
EMAIL_FILE = "data.csv"


def load_dataframes():
    portal_df = pd.read_csv(PORTAL_FILE)
    client_df = pd.read_csv(CLIENT_FILE)
    email_df = pd.read_csv(EMAIL_FILE)
    return portal_df, client_df, email_df


def find_mismatches(portal_df, client_df):
    return pd.merge(
        portal_df,
        client_df,
        on=["Client_Name", "GSTIN", "Invoice_Number", "Amount"],
        how="outer",
        indicator=True,
    )


def build_alerts(mismatch_df, email_df, merge_label, message_builder):
    filtered = mismatch_df[mismatch_df["_merge"] == merge_label].copy()
    alerts = filtered.merge(email_df, on="Client_Name", how="left")
    alerts["message"] = alerts.apply(message_builder, axis=1)
    return alerts


def client_message(row):
    return (
        f"Alert: {row['Client_Name']} needs to submit Invoice "
        f"{row['Invoice_Number']} for Rs.{row['Amount']}"
    )


def portal_message(row):
    return (
        f"Alert: {row['Client_Name']} submitted Invoice {row['Invoice_Number']}, "
        "but it's not on the GST portal."
    )


def print_alerts(title, alerts_df):
    print(f"\n--- {title} ---")
    if alerts_df.empty:
        print("No alerts.")
        return

    for _, row in alerts_df.iterrows():
        print(row["message"])
        if pd.isna(row.get("Email")):
            print("  Email not found for this client.")
        else:
            print(f"  Email: {row['Email']}")


def get_smtp_credentials():
    load_dotenv()
    sender = os.getenv("EMAIL_SENDER")
    password = os.getenv("EMAIL_PASSWORD")

    if not sender or not password:
        raise ValueError(
            "EMAIL_SENDER and EMAIL_PASSWORD must be set in the environment or .env file."
        )

    return sender, password


def send_email(smtp, sender, receiver, subject, body):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = receiver
    msg.set_content(body)
    smtp.send_message(msg)


def send_alerts(alerts_df, subject):
    if alerts_df.empty:
        print(f"No emails to send for: {subject}")
        return

    sender, password = get_smtp_credentials()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender, password)

        for _, row in alerts_df.iterrows():
            receiver = row.get("Email")
            if pd.isna(receiver):
                print(f"Skipping {row['Client_Name']}: no email address found.")
                continue

            send_email(smtp, sender, receiver, subject, row["message"])
            print(f"Email sent to {receiver}")


def main(send_emails=False):
    portal_df, client_df, email_df = load_dataframes()
    mismatch_df = find_mismatches(portal_df, client_df)

    missing_from_client = build_alerts(
        mismatch_df,
        email_df,
        "left_only",
        client_message,
    )
    missing_from_portal = build_alerts(
        mismatch_df,
        email_df,
        "right_only",
        portal_message,
    )

    print_alerts("ACTION REQUIRED: CLIENT FORGOT TO SUBMIT", missing_from_client)
    print_alerts("ACTION REQUIRED: MISSING ON PORTAL", missing_from_portal)

    if send_emails:
        send_alerts(missing_from_client, "Reminder for missing invoices")
        send_alerts(missing_from_portal, "Reminder to update bills on portal")


if __name__ == "__main__":
    main(send_emails=True)
