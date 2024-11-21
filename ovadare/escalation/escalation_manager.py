# ovadare/escalation/escalation_manager.py

"""
Escalation Manager Module for the Ovadare Framework

This module provides the EscalationManager class, which handles the escalation
of unresolved conflicts by notifying administrators via email and SMS. It
integrates with external services like SendGrid and Twilio, using the
SecretsManager to securely manage API keys and credentials.
"""

import logging
from typing import List, Dict, Any
from ovadare.conflicts.conflict import Conflict
from ovadare.utils.secrets_manager import SecretsManager

# Third-party libraries for sending emails and SMS
import sendgrid
from sendgrid.helpers.mail import Mail
from twilio.rest import Client

# Configure the logger for this module
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class EscalationManager:
    """
    Handles escalation of unresolved conflicts by notifying administrators.
    """

    def __init__(self, secrets_manager: SecretsManager) -> None:
        """
        Initializes the EscalationManager.

        Args:
            secrets_manager (SecretsManager): Manages secure access to API keys and credentials.
        """
        self.secrets_manager = secrets_manager
        self.admin_emails = self._get_admin_emails()
        self.admin_phone_numbers = self._get_admin_phone_numbers()
        self.sendgrid_api_key = self.secrets_manager.get_secret('SENDGRID_API_KEY')
        self.twilio_account_sid = self.secrets_manager.get_secret('TWILIO_ACCOUNT_SID')
        self.twilio_auth_token = self.secrets_manager.get_secret('TWILIO_AUTH_TOKEN')
        self.twilio_phone_number = self.secrets_manager.get_secret('TWILIO_PHONE_NUMBER')
        logger.debug("EscalationManager initialized with notification services.")

    def escalate_conflict(self, conflict: Conflict) -> None:
        """
        Escalates an unresolved conflict by notifying administrators.

        Args:
            conflict (Conflict): The conflict to escalate.
        """
        logger.info(f"Escalating conflict '{conflict.conflict_id}'.")
        email_subject = f"Urgent: Conflict {conflict.conflict_id} Requires Attention"
        email_body = f"A conflict has been detected and requires immediate attention.\n\nDetails:\n{conflict}"
        sms_message = f"Conflict {conflict.conflict_id} requires attention. Check your email for details."

        # Send notifications
        self._send_email(subject=email_subject, body=email_body)
        self._send_sms(message=sms_message)

    def _send_email(self, subject: str, body: str) -> None:
        """
        Sends an email notification to administrators.

        Args:
            subject (str): The email subject.
            body (str): The email body.
        """
        if not self.sendgrid_api_key:
            logger.error("SendGrid API key is missing. Cannot send email notifications.")
            return

        sg = sendgrid.SendGridAPIClient(api_key=self.sendgrid_api_key)
        for admin_email in self.admin_emails:
            try:
                mail = Mail(
                    from_email='noreply@ovadare.com',
                    to_emails=admin_email,
                    subject=subject,
                    plain_text_content=body
                )
                response = sg.send(mail)
                if response.status_code in [200, 202]:
                    logger.info(f"Email notification sent to {admin_email}.")
                else:
                    logger.error(f"Failed to send email to {admin_email}: {response.status_code}")
            except Exception as e:
                logger.error(f"Exception occurred while sending email to {admin_email}: {e}")

    def _send_sms(self, message: str) -> None:
        """
        Sends an SMS notification to administrators.

        Args:
            message (str): The SMS message content.
        """
        if not all([self.twilio_account_sid, self.twilio_auth_token, self.twilio_phone_number]):
            logger.error("Twilio credentials are missing. Cannot send SMS notifications.")
            return

        client = Client(self.twilio_account_sid, self.twilio_auth_token)
        for admin_phone in self.admin_phone_numbers:
            try:
                sms = client.messages.create(
                    body=message,
                    from_=self.twilio_phone_number,
                    to=admin_phone
                )
                logger.info(f"SMS notification sent to {admin_phone}. SID: {sms.sid}")
            except Exception as e:
                logger.error(f"Exception occurred while sending SMS to {admin_phone}: {e}")

    def _get_admin_emails(self) -> List[str]:
        """
        Retrieves the list of administrator email addresses.

        Returns:
            List[str]: A list of admin email addresses.
        """
        emails = self.secrets_manager.get_secret('ADMIN_EMAILS')
        if emails:
            admin_emails = emails.split(',')
            logger.debug(f"Admin emails retrieved: {admin_emails}")
            return admin_emails
        else:
            logger.warning("No admin emails configured.")
            return []

    def _get_admin_phone_numbers(self) -> List[str]:
        """
        Retrieves the list of administrator phone numbers.

        Returns:
            List[str]: A list of admin phone numbers.
        """
        phones = self.secrets_manager.get_secret('ADMIN_PHONE_NUMBERS')
        if phones:
            admin_phones = phones.split(',')
            logger.debug(f"Admin phone numbers retrieved: {admin_phones}")
            return admin_phones
        else:
            logger.warning("No admin phone numbers configured.")
            return []
