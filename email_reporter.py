import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
import os


def send_anomaly_report(
    monitoring_results, receiver_email=None
):
    """
    Send an email report with all detected anomalies and file changes

    Args:
        monitoring_results: Dictionary containing anomalies, added, deleted, modified files
        receiver_email: Email address to send the report to (default from env var)
    """
    # Get email configuration from environment variables
    sender_email = os.environ.get('SHADOWTRACE_EMAIL', 'your-email@gmail.com')
    sender_password = os.environ.get('SHADOWTRACE_PASSWORD', '')
    
    if not receiver_email:
        receiver_email = os.environ.get('SHADOWTRACE_RECEIVER', 'alerts@example.com')
    
    # Validate email configuration
    if not sender_password or sender_email == 'your-email@gmail.com':
        print("\n⚠️  Email not configured!")
        print("Please set environment variables:")
        print("  SHADOWTRACE_EMAIL - Your Gmail address")
        print("  SHADOWTRACE_PASSWORD - Your Gmail app password")
        print("  SHADOWTRACE_RECEIVER - Recipient email address")
        return False
    
    subject = "🔒 ShadowTrace Security Alert - Anomalies Detected"

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject

    # Create detailed email body
    email_body = generate_report_text(monitoring_results)

    msg.attach(MIMEText(email_body, "plain"))

    try:
        # Send email
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()

        print("\n✅ Email report sent successfully!")
        print(f"   From: {sender_email}")
        print(f"   To: {receiver_email}")
        return True
    except Exception as e:
        print(f"\n❌ Failed to send email: {str(e)}")
        print("\nTroubleshooting:")
        print("  1. Check your email and password are correct")
        print("  2. For Gmail, use an App Password (not your regular password)")
        print("  3. Enable 2-Factor Authentication in your Google Account")
        print("  4. Generate App Password: Google Account > Security > App Passwords")
        return False


def generate_report_text(results):
    """Generate formatted email report text"""

    report = f"""
╔══════════════════════════════════════════════════════════════╗
║           SHADOWTRACE MONITORING REPORT                      ║
╚══════════════════════════════════════════════════════════════╝

📅 Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
📁 Monitored Directory: {results['directory']}
🔄 Total Scans Completed: {results['total_scans']}

"""

    # Anomalies Section
    report += "\n" + "=" * 60 + "\n"
    report += "⚠️  SECURITY ANOMALIES DETECTED\n"
    report += "=" * 60 + "\n"

    if results["anomalies"]:
        report += f"\n🚨 TOTAL ANOMALIES: {len(results['anomalies'])}\n\n"
        for i, anomaly in enumerate(results["anomalies"], 1):
            report += f"{i}. {anomaly}\n"
    else:
        report += "\n✅ No anomalies detected during monitoring period.\n"

    # File Changes Section
    report += "\n\n" + "=" * 60 + "\n"
    report += "📊 FILE CHANGE SUMMARY\n"
    report += "=" * 60 + "\n\n"

    # Added Files
    if results["added"]:
        report += f"✅ ADDED FILES ({len(results['added'])}):\n"
        for f in results["added"]:
            report += f"   + {f['full_path']}\n"
            report += f"     Size: {format_file_size(f['file_size'])}\n"
            report += f"     Created: {f['creation_time']}\n\n"
    else:
        report += "✅ Added Files: None\n\n"

    # Deleted Files
    if results["deleted"]:
        report += f"🗑️  DELETED FILES ({len(results['deleted'])}):\n"
        for f in results["deleted"]:
            report += f"   - {f['full_path']}\n\n"
    else:
        report += "🗑️  Deleted Files: None\n\n"

    # Modified Files
    if results["modified"]:
        report += f"📝 MODIFIED FILES ({len(results['modified'])}):\n"
        for f in results["modified"]:
            report += f"   ~ {f['full_path']}\n"
            report += f"     Size: {format_file_size(f['file_size'])}\n"
            report += f"     Last Modified: {f['modified_time']}\n\n"
    else:
        report += "📝 Modified Files: None\n\n"

    # Summary
    report += "\n" + "=" * 60 + "\n"
    report += "📈 STATISTICS\n"
    report += "=" * 60 + "\n"
    report += f"Total Files Added: {len(results['added'])}\n"
    report += f"Total Files Deleted: {len(results['deleted'])}\n"
    report += f"Total Files Modified: {len(results['modified'])}\n"
    report += f"Total Anomalies: {len(results['anomalies'])}\n"

    if results["anomalies"]:
        report += "\n⚠️  ACTION REQUIRED: Review the anomalies listed above.\n"
    else:
        report += "\n✅ System Status: Normal - No suspicious activity detected.\n"

    report += """

─────────────────────────────────────────────────────────────
Thank you for using ShadowTrace File Monitoring System.

Best regards,
ShadowTrace Security Team
─────────────────────────────────────────────────────────────
"""

    return report


def format_file_size(size_bytes):
    """Format file size in human-readable format"""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"


#  Send simple notification email
def send_simple_email(text, subject="ShadowTrace Notification"):
    """Send a simple text email"""
    sender_email = os.environ.get('SHADOWTRACE_EMAIL', 'your-email@gmail.com')
    sender_password = os.environ.get('SHADOWTRACE_PASSWORD', '')
    receiver_email = os.environ.get('SHADOWTRACE_RECEIVER', 'alerts@example.com')
    
    if not sender_password or sender_email == 'your-email@gmail.com':
        print("⚠️  Email not configured! Set environment variables first.")
        return False

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject

    msg.attach(MIMEText(text, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        print("✅ Email sent successfully!")
        return True
    except Exception as e:
        print(f"❌ Failed to send email: {str(e)}")
        return False