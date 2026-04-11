import re
from bs4 import BeautifulSoup

def clean_email_text(raw_text):
    if not isinstance(raw_text, str):
        return ""

    text = re.sub(r'^\s*(?:From|To|Subject|Received|Date|Message-ID|MIME-Version|Content-Type|X-.*):.*$', '', raw_text, flags=re.MULTILINE | re.IGNORECASE)
    text = BeautifulSoup(text, "html.parser").get_text(separator=" ")
    text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '[URL]', text)
    text = re.sub(r'\s+', ' ', text)

    return text.strip()

if __name__ == "__main__":
    mail_sale = """
    Received: by 10.10.10.10 with SMTP id abcdef; Tue, 11 Apr 2026 09:00:00 -0700
    From: "Admin" <hacker@fake-paypal.com>
    To: victim@company.com
    Content-Type: text/html; charset="UTF-8"

    <html>
        <body>
            <h1>Alerte de sécurité !</h1>
            <p>Votre compte a été suspendu. Cliquez sur ce lien pour le débloquer : 
            <a href="https://very-bad-website.com/login?token=123456789">Débloquer mon compte</a></p>
            <br>
            <div class="footer">
                <script>console.log("tracking malware")</script>
                Merci de votre confiance.
            </div>
        </body>
    </html>
    """

    print("=== AVANT LE NETTOYAGE ===")
    print(mail_sale)
    print("\n=== APRÈS LE NETTOYAGE ===")
    print(clean_email_text(mail_sale))