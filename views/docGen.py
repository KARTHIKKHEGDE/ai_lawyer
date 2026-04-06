import os
import re
from docx import Document as DocxDocument
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

templates = {
    "bail_application": """\
[COURT NAME]
[COURT ADDRESS]

[Bail Application No. XYZ]
Date: [DATE]

To,
The Hon'ble Judge,
[COURT NAME]

Re: Bail Application for [APPLICANT NAME] (Case No. [CASE NUMBER])

Dear Sir/Madam,

I, [YOUR NAME], am writing to you in my capacity as the [relation to applicant, e.g., family member, friend, legal counsel] of [APPLICANT NAME], who is currently charged with [OFFENSE] under [SECTION] of the Indian Penal Code (IPC). The charges stem from an incident that occurred on [DATE OF INCIDENT], and I wish to present this application for bail on the following grounds:

1. **Nature of the Offense**: [Briefly describe the nature of the offense and any mitigating circumstances that may apply. If the offense is bailable under IPC, specify it.]

2. **Non-flight Risk**: [Explain why the applicant is not a flight risk. Include details such as employment status, family ties, and community ties.]

3. **Cooperation with Investigation**: [Highlight any cooperation the applicant has shown during the investigation, such as attending police summons or providing statements.]

4. **Health and Well-being**: [Mention any health issues the applicant may have that necessitate their release on bail, if applicable.]

5. **Grounds for Bail**: [List any other pertinent factors that support the request for bail, such as lack of prior convictions, good character references, etc.]

In light of these considerations, I respectfully urge your Honour to grant bail to [APPLICANT NAME]. I assure you that the applicant will adhere to all conditions set forth by the court.

Thank you for your kind consideration.

Sincerely,
[YOUR NAME]
[YOUR ADDRESS]
[YOUR CONTACT]
""",
    "lease_agreement": """\
LEASE AGREEMENT

This Lease Agreement ("Agreement") is made and entered into on this [DATE] by and between [LANDLORD NAME], residing at [LANDLORD ADDRESS] (hereinafter referred to as the "Landlord"), and [TENANT NAME], residing at [TENANT ADDRESS] (hereinafter referred to as the "Tenant").

WHEREAS, the Landlord is the lawful owner of the residential property located at [PROPERTY ADDRESS] (hereinafter referred to as the "Property"), and

WHEREAS, the Tenant wishes to lease the Property from the Landlord for residential purposes,

NOW, THEREFORE, in consideration of the mutual promises contained herein, the parties agree as follows:

1. **Property Address**: The Landlord hereby leases to the Tenant the Property situated at [PROPERTY ADDRESS].

2. **Lease Term**: This lease shall commence on [START DATE] and shall continue until [END DATE] unless terminated earlier in accordance with this Agreement.

3. **Monthly Rent**: The Tenant agrees to pay a monthly rent of ₹[MONTHLY RENT], payable in advance on or before the [DUE DATE] of each month.

4. **Security Deposit**: The Tenant shall pay a security deposit of ₹[SECURITY DEPOSIT] prior to taking possession of the Property. This deposit shall be refunded upon termination of this lease, subject to any deductions for damages or unpaid dues.

5. **Maintenance Responsibilities**: 
   - The Landlord shall be responsible for the maintenance of the Property, including repairs to plumbing, electrical, and structural issues.
   - The Tenant shall maintain the Property in a clean and sanitary condition and shall be responsible for minor repairs.

6. **Late Payment Penalty**: Any rent not received within [NUMBER OF DAYS] days of the due date shall incur a late fee of ₹[LATE PAYMENT PENALTY].

7. **Subletting Clause**: The Tenant shall not sublet the Property or assign this Agreement without the prior written consent of the Landlord.

8. **Termination**: Either party may terminate this Agreement by providing [NUMBER OF DAYS] days' written notice to the other party.

9. **Governing Law**: This Agreement shall be governed by and construed in accordance with the laws of India.

IN WITNESS WHEREOF, the parties have executed this Lease Agreement as of the date first above written.

**Signatures**:
Landlord: ________________  Date: __________
Tenant: ________________    Date: __________
Witness 1: ________________  Date: __________
Witness 2: ________________  Date: __________


""",

    "cease_and_desist": """\
[YOUR LAW FIRM NAME]
[YOUR LAW FIRM ADDRESS]
[PHONE NUMBER]
[EMAIL]

Date: [DATE]

To,
[RECIPIENT NAME]
[RECIPIENT ADDRESS]

Subject: Cease and Desist for Copyright Infringement

Dear [RECIPIENT NAME],

We represent [YOUR CLIENT NAME], the owner of certain copyrighted material, including [DESCRIPTION OF COPYRIGHTED MATERIAL]. It has come to our attention that you have been engaging in activities that infringe upon our client's copyright, specifically [DESCRIPTION OF INFRINGEMENT].

As you are likely aware, such unauthorized use constitutes a violation of the Copyright Act, 1957, and may expose you to legal liability.

We hereby demand that you:

1. Immediately cease and desist all infringing activities, including but not limited to [SPECIFIC ACTIVITIES].
2. Provide us with written confirmation of your compliance by [DEADLINE].

Failure to comply with this demand may result in legal action against you, including seeking damages and injunctive relief.

We hope to resolve this matter amicably. Please contact us at your earliest convenience to discuss this matter further.

Sincerely,
[YOUR NAME]
[YOUR TITLE]
[YOUR LAW FIRM NAME]
[YOUR CONTACT]


""",

    "power_of_attorney": """\
POWER OF ATTORNEY

This Power of Attorney ("POA") is executed on this [DATE] by [PRINCIPAL NAME], residing at [PRINCIPAL ADDRESS] (hereinafter referred to as the "Principal"), appointing [AGENT NAME], residing at [AGENT ADDRESS], as my attorney-in-fact (hereinafter referred to as the "Agent").

WHEREAS, the Principal desires to appoint the Agent to act on their behalf in legal and financial matters, and

WHEREAS, the Agent agrees to accept such appointment under the terms and conditions set forth in this document,

NOW, THEREFORE, the Principal hereby grants the Agent the following powers:

1. **Authority**: The Agent shall have full power and authority to act on behalf of the Principal in the following matters:
   - Managing bank accounts, including deposits and withdrawals.
   - Buying, selling, and managing real estate.
   - Handling legal matters, including but not limited to initiating or defending lawsuits.
   - Making healthcare decisions in accordance with the Principal's wishes.

2. **Effective Date**: This Power of Attorney shall be effective immediately upon execution and shall continue until revoked by the Principal.

3. **Revocation**: The Principal may revoke this Power of Attorney at any time by providing written notice to the Agent. Such revocation shall not affect any actions taken by the Agent prior to receipt of the revocation notice.

4. **Indemnification**: The Principal agrees to indemnify and hold harmless the Agent from any liability arising from actions taken in good faith under this Power of Attorney.

5. **Governing Law**: This POA shall be governed by and construed in accordance with the laws of India.

IN WITNESS WHEREOF, the Principal has executed this Power of Attorney as of the date first above written.

**Signatures**:
Principal: ________________  Date: __________
Agent: ________________      Date: __________
Witness 1: ________________  Date: __________
Witness 2: ________________  Date: __________

"""
}

def extract_details_with_ai(prompt, document_type):
    """
    Use AI to extract specific details from user prompt for document generation.
    """
    extraction_prompt = f"""
    Extract specific details from this user request for a {document_type}:
    "{prompt}"
    
    Return ONLY a JSON object with the following fields (use "NOT_PROVIDED" if not mentioned):
    {{
        "applicant_name": "person's name who needs bail",
        "offense": "what crime/charge",
        "section": "IPC section number",
        "court_name": "which court",
        "case_number": "case number if mentioned",
        "date_of_incident": "when did the incident happen",
        "lawyer_name": "lawyer's name",
        "your_name": "who is applying (if different from lawyer)",
        "relationship": "relationship to applicant",
        "additional_details": "any other specific details mentioned"
    }}
    
    Example: If user says "bail application for John charged with theft under section 379"
    Return: {{"applicant_name": "John", "offense": "theft", "section": "379", "court_name": "NOT_PROVIDED", ...}}
    """
    
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(extraction_prompt)
        import json
        extracted_data = json.loads(response.text.strip())
        return extracted_data
    except Exception as e:
        print(f"AI extraction failed: {e}")
        return {}
def get_document_requirements(doc_type):
    """
    Returns what information is needed for each document type.
    """
    requirements = {
        "bail_application": [
            "📝 Required: Applicant's full name",
            "⚖️ Required: Type of offense/charge",
            "📖 Required: IPC section number", 
            "🏛️ Required: Court name (e.g., 'Delhi District Court')",
            "📋 Optional: Case number",
            "👤 Optional: Lawyer/applicant name",
            "📅 Optional: Date of incident",
            "\n💡 Example: 'bail application for John Doe charged with theft under section 379 at Delhi District Court case number CR-123/2024 by lawyer Priya Sharma'"
        ],
        "lease_agreement": [
            "🏠 Required: Property address",
            "👤 Required: Landlord name", 
            "👤 Required: Tenant name",
            "💰 Required: Monthly rent amount",
            "📅 Required: Lease start/end dates"
        ]
    }
    return requirements.get(doc_type, ["Please provide specific details for the document."])

def generate_legal_document(prompt, save_dir='static/generated_docs'):
    """
    Generates a legal document Word file based on the given prompt.
    Now uses AI to extract specific details from user input.
    
    Args:
        prompt (str): User input specifying type and details.
        save_dir (str): Directory where the document will be saved.

    Returns:
        (str, str): file path, file name
    """

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    prompt_lower = prompt.lower()
    file_name = ""
    template = ""
    
    # Determine document type
    if any(word in prompt_lower for word in ["bail", "bail application"]):
        template = templates["bail_application"]
        file_name = "bail_application.docx"
        doc_type = "bail_application"
        
    elif any(word in prompt_lower for word in ["lease", "lease agreement", "rental"]):
        template = templates["lease_agreement"]
        file_name = "lease_agreement.docx"
        doc_type = "lease_agreement"
        
    elif any(word in prompt_lower for word in ["cease", "cease and desist", "copyright"]):
        template = templates["cease_and_desist"]
        file_name = "cease_and_desist.docx"
        doc_type = "cease_and_desist"
        
    elif any(word in prompt_lower for word in ["power of attorney", "poa"]):
        template = templates["power_of_attorney"]
        file_name = "power_of_attorney.docx"
        doc_type = "power_of_attorney"
    else:
        # If no specific type detected, provide requirements guide
        if any(word in prompt_lower for word in ["help", "what", "how", "requirements"]):
            requirements_text = "\n".join([
                "📋 **Document Generation Requirements:**\n",
                "🎯 **Bail Application:**",
                *get_document_requirements("bail_application"),
                "\n🎯 **Other Documents:** lease agreement, cease and desist, power of attorney"
            ])
            raise ValueError(requirements_text)
        elif len(prompt.strip()) < 10:
            raise ValueError(f"Please provide more details.\n\n{chr(10).join(get_document_requirements('bail_application'))}")
        else:
            raise ValueError("Unsupported document type. Supported: bail application, lease agreement, cease and desist, power of attorney.\n\nType 'help' for requirements.")

    # Extract details using AI
    extracted_data = extract_details_with_ai(prompt, doc_type)
    
    # Build data dictionary with extracted info or defaults
    if doc_type == "bail_application":
        data = {
            "COURT NAME": extracted_data.get("court_name") if extracted_data.get("court_name") != "NOT_PROVIDED" else "[COURT NAME - Please specify]",
            "COURT ADDRESS": "[COURT ADDRESS - Please specify]",
            "APPLICANT NAME": extracted_data.get("applicant_name") if extracted_data.get("applicant_name") != "NOT_PROVIDED" else "[APPLICANT NAME - Please specify]",
            "YOUR NAME": extracted_data.get("lawyer_name", extracted_data.get("your_name")) if extracted_data.get("lawyer_name") != "NOT_PROVIDED" else "[YOUR NAME - Please specify]",
            "relation to applicant, e.g., family member, friend, legal counsel": extracted_data.get("relationship") if extracted_data.get("relationship") != "NOT_PROVIDED" else "legal counsel",
            "OFFENSE": extracted_data.get("offense") if extracted_data.get("offense") != "NOT_PROVIDED" else "[OFFENSE - Please specify]",
            "SECTION": extracted_data.get("section") if extracted_data.get("section") != "NOT_PROVIDED" else "[IPC SECTION - Please specify]",
            "DATE OF INCIDENT": extracted_data.get("date_of_incident") if extracted_data.get("date_of_incident") != "NOT_PROVIDED" else "[DATE OF INCIDENT - Please specify]",
            "CASE NUMBER": extracted_data.get("case_number") if extracted_data.get("case_number") != "NOT_PROVIDED" else "[CASE NUMBER - Please specify]",
            "DATE": "[TODAY'S DATE - Please specify]",
            "YOUR ADDRESS": "[YOUR ADDRESS - Please specify]",
            "YOUR CONTACT": "[YOUR CONTACT - Please specify]"
        }
    
    # Add handling for other document types here...
    else:
        data = {}  # Will be filled for other document types

    # Fill in template
    document_content = template
    for key, value in data.items():
        document_content = document_content.replace(f"[{key}]", str(value))

    # Create document
    doc = DocxDocument()
    for line in document_content.split("\n"):
        if line.strip():
            doc.add_paragraph(line)

    file_path = os.path.join(save_dir, file_name)
    doc.save(file_path)

    return file_path, file_name
