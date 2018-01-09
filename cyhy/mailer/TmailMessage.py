import pystache

from cyhy.mailer.Message import Message
from cyhy.mailer.ReportMessage import ReportMessage


class TmailMessage(ReportMessage):
    """A class representing an email message with a Trustworthy Email
    report PDF attachment.

    Static attributes
    -----------------
    Subject : str
        The mustache template to use when constructing the message
        subject.

    TextBody : str
        The mustache template to use when constructing the plain text
        message body.

    HtmlBody : str
        The mustache template to use when constructing the HTML
        message body.
    """

    Subject = '{{acronym}} - Trustworthy Email Report - {{report_date}} Results'

    TextBody = '''Greetings {{acronym}},

Attached is your Trustworthy Email Report. This report presents your organization's use of SPF, DMARC, and STARTTLS, as discovered at your .gov domains. The data in this report comes from a scan that took place on {{report_date}}.

DHS Binding Operational Directive 18-01 requires your agency to take certain actions relevant to the data in this report:
* By January 15, 2018:
  * Configure all second-level domains to have valid SPF/DMARC records, with at minimum a DMARC policy of "p=none".
  * "reports@dmarc.cyber.dhs.gov" must be added as a recipient of aggregate reports.
  * Internet-facing mail servers must offer STARTTLS.
* By October 16, 2018:
  * A DMARC policy of reject must be set for all second-level domains and mail-sending hosts.

Raw results in this Report are available as a CSV in the Appendix, which includes error messages. Note that this report includes data from second-level .gov domains, but the Directive's scope includes any domain suffix.

See https://cyber.dhs.gov/intro for more information about email authentication, and https://cyber.dhs.gov/guide for a compliance checklist and FAQ.

If you believe our reporting or methodology is in error, let us know. If the flaw appears tool-related, we encourage you to file an issue on our open-source scanner at https://github.com/dhs-ncats/trustymail.

We welcome your feedback and questions.

Cheers,
The NCATS Team

National Cybersecurity Assessments and Technical Services (NCATS)
National Cybersecurity & Communications Integration Center
U.S. Department of Homeland Security
ncats@hq.dhs.gov

----changelog----
1/09/2018
* Added: STARTTLS tracking, BOD scoring of available data, SPF tracking solely for second-level domains and SMTP-responsive subdomains

12/11/2017
* Known issue: The fed.us TLD is inaccurately represented in some reports.
--------------------
'''

    HtmlBody = '''<html>
<head></head>
<body>  
<div style=""font-size:14.5"">
<p>Greetings {{acronym}},</p>
<p>Attached is your <b>Trustworthy Email Report</b>. This report presents your organization's use of SPF, DMARC, and STARTTLS, as discovered at your .gov domains. The data in this report comes from a <b>scan that took place on {{report_date}}.</b></p>
<p><a href="https://cyber.dhs.gov">DHS Binding Operational Directive 18-01</a> requires your agency to take certain actions relevant to the data in this report:</p>
<p><i>By January 15, 2018</i>:
<ul>
<li>Configure all second-level domains to have valid SPF/DMARC records, with at minimum a DMARC policy of &ldquo;p=none&rdquo;.</li>
<li>&ldquo;reports@dmarc.cyber.dhs.gov&rdquo; <a href="https://cyber.dhs.gov/guide/#dhs-dmarc-reporting-location">must be added as a recipient of aggregate reports</a>.</li>
<li>Internet-facing mail servers must offer STARTTLS.</li>
</ul>
<i>By October 16, 2018</i>:
<ul>
<li>A DMARC policy of reject must be set for all second-level domains and mail-sending hosts.</li>
</ul>
</p>
<p>Raw results in this Report are available as a CSV in the Appendix, which includes error messages. Note that this report includes data from second-level .gov domains, but the Directive's <a href="https://cyber.dhs.gov/guide/#what-is-the-scope-of-bod-18-01">scope includes any domain suffix</a>.</p>
<p>See <a href="https://cyber.dhs.gov/intro">cyber.dhs.gov/intro</a> for more information about email authentication, and <a href="https://cyber.dhs.gov/guide">cyber.dhs.gov/guide</a> for a compliance checklist and FAQ.</p>
<p>If you believe our reporting or methodology is in error, let us know. If the flaw appears tool-related, we encourage you to <a href="https://github.com/dhs-ncats/trustymail">file an issue</a> on our open-source scanner.</p>
<p>We welcome your feedback and questions.</p>
Cheers,<br>
The NCATS Team<br><br />
National Cybersecurity Assessments and Technical Services (NCATS)<br />
National Cybersecurity & Communications Integration Center<br/>
U.S. Department of Homeland Security <br/>
<a href=""mailto:ncats@hq.dhs.gov""> ncats@hq.dhs.gov </a> </p>
</div></p><br>
<p>----changelog----</p>
<p><i>1/09/2018</i></p>
<p><b>* Added:</b> STARTTLS tracking, BOD scoring of available data, SPF tracking solely for second-level domains and SMTP-responsive subdomains<br></p>
<p><i>12/11/2017</i></p>
<b>* Known issue:</b> The fed.us TLD is inaccurately represented in some reports.</p>
<p>--------------------</p>
</body>
</html>
'''

    def __init__(self, to_addrs, pdf_filename, agency_acronym, report_date, from_addr=Message.DefaultFrom, cc_addrs=Message.DefaultCc):
        """Construct an instance.

        Parameters
        ----------
        to_addrs : array of str
            An array of string objects, each of which is an email
            address to which this message should be sent.

        pdf_filename : str
            The filename of the PDF file that is the Trustworthy Email
            report corresponding to this message.

        agency_acronym : str
            The acronym used by the agency corresponding to the
            Trustworthy Email report attachment.

        report_date : str
            The date corresponding to the Trustworthy Email report
            attachment.  We have been using dates of the form December
            12, 2017.

        from_addr : str
            The email address from which this message is to be sent.

        cc_addrs : array of str
            An array of string objects, each of which is a CC email
            address to which this message should be sent.
        """
        # This is the data mustache will use to render the templates
        mustache_data = {
            'acronym': agency_acronym,
            'report_date': report_date
        }

        # Render the templates
        subject = pystache.render(TmailMessage.Subject, mustache_data)
        text_body = pystache.render(TmailMessage.TextBody, mustache_data)
        html_body = pystache.render(TmailMessage.HtmlBody, mustache_data)

        ReportMessage.__init__(self, to_addrs, subject, text_body, html_body, pdf_filename, from_addr, cc_addrs)
