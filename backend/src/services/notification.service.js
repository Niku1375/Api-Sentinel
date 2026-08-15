const nodemailer = require('nodemailer');
const config = require('../config');

const transporter = nodemailer.createTransport({
  host: config.SMTP_HOST,
  port: config.SMTP_PORT,
  auth: { user: config.SMTP_USER, pass: config.SMTP_PASSWORD },
});

async function sendEmailAlert(toEmail, subject, message) {
  try {
    await transporter.sendMail({
      from: config.EMAIL_FROM,
      to: toEmail,
      subject,
      text: message,
    });
    console.log(`[Email sent] Subject: ${subject} To: ${toEmail}`);
  } catch (err) {
    console.error(`[Email failed] Subject: ${subject} To: ${toEmail} Error: ${err.message}`);
  }
}

module.exports = { sendEmailAlert };
