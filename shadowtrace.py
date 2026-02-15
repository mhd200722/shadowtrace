import file_monitor
from pyfiglet import figlet_format
from termcolor import colored
import email_reporter

print(colored(figlet_format("ShadowTrace"), color="magenta"))
print(colored("=" * 60, color="white"))
print(colored("    File Monitoring & Anomaly Detection System", color="cyan"))
print(colored("=" * 60, color="white"))
print()


# Get user inputs
path = input(colored("📁 Enter Your Path Directory: ", color="white"))
num_of_scan = int(
    input(colored("🔄 Enter Number Of Scans (Default: 10): ", color="white")) or "10"
)
scan_interval = int(
    input(colored("⏱️  Enter Scan Interval in seconds (Default: 60): ", color="white"))
    or "60"
)
email_option = (
    input(colored("📧 Send email report after completion? [Y/N]: ", color="white"))
    .strip()
    .upper()
)
if email_option=="Y":
    reciever_email=(input(colored("✉️ Enter Your Email: ", color="white"))
    .strip())
    print(colored("\n📧 Preparing email report...", color="cyan"))
    
else:
    print(colored("\n⚠️  Invalid option. Email not sent.", color="red"))


print("\n" + colored("=" * 60, color="green"))
print(colored("🔍 Starting monitoring...", color="green"))
print(colored("=" * 60, color="green"))
print(f"📂 Folder: {path}")
print(f"🔄 Scans: {num_of_scan}")
print(f"⏱️  Interval: {scan_interval} seconds")
print(colored("=" * 60, color="green"))

monitoring_results = file_monitor.monitor_directory(
    path, number_of_scans=num_of_scan, scan_interval=scan_interval
)


print("\n" + colored("=" * 60, color="green"))
print(colored("✅ Monitoring completed!", color="green"))
print(colored("=" * 60, color="green"))


# Display summary
print(f"\n📊 MONITORING SUMMARY:")
print(f"   • Total Anomalies: {len(monitoring_results['anomalies'])}")
print(f"   • Files Added: {len(monitoring_results['added'])}")
print(f"   • Files Deleted: {len(monitoring_results['deleted'])}")
print(f"   • Files Modified: {len(monitoring_results['modified'])}")

# Send email if requested
if email_option == "Y":
    
    

    if monitoring_results["anomalies"]:
        print(
            colored("⚠️  Anomalies detected! Sending security alert...", color="yellow")
        )

    success = email_reporter.send_anomaly_report(monitoring_results,receiver_email=reciever_email)

    if success:
        print(colored("✅ Email report sent successfully!", color="green"))
    else:
        print(
            colored(
                "❌ Failed to send email. Check your internet connection.", color="red"
            )
        )
elif email_option == "N":
    print(colored("\n📧 Email report skipped.", color="yellow"))
else:
    print(colored("\n⚠️  Invalid option. Email not sent.", color="red"))

print("\n" + colored("=" * 60, color="magenta"))
print(colored("Thank you for using ShadowTrace! 🛡️", color="magenta"))
print(colored("=" * 60, color="magenta"))
