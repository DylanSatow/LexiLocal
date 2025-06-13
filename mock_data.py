#!/usr/bin/env python3

# Mock legal document data for development
MOCK_LEGAL_DOCS = [
    {
        "id": "001",
        "title": "Johnson v. Smith",
        "citation": "123 F.3d 456 (9th Cir. 2020)",
        "docket_number": "20-1234",
        "state": "CA",
        "issuer": "United States Court of Appeals for the Ninth Circuit",
        "document": """
UNITED STATES COURT OF APPEALS FOR THE NINTH CIRCUIT

JOHNSON v. SMITH

No. 20-1234

Appeal from the United States District Court
for the Northern District of California

OPINION

This case involves a contract dispute between Johnson and Smith regarding the sale of commercial property. The plaintiff, Johnson, alleges that the defendant, Smith, breached their purchase agreement by failing to complete the transaction within the specified timeframe.

FACTS

On January 15, 2019, Johnson and Smith entered into a purchase agreement for commercial property located at 123 Main Street, San Francisco, California. The agreement stipulated that the transaction must be completed by March 15, 2019, with a purchase price of $2,500,000.

Smith failed to secure financing by the deadline and requested an extension. Johnson refused the extension and demanded specific performance or damages.

LEGAL ANALYSIS

Under California contract law, time is of the essence clauses are strictly enforced when the parties explicitly agree to such terms. The purchase agreement clearly stated that "time is of the essence" regarding all performance deadlines.

The court finds that Smith materially breached the contract by failing to complete the purchase within the specified timeframe. Johnson is entitled to damages resulting from this breach.

CONCLUSION

The district court's judgment in favor of Johnson is AFFIRMED. Smith is liable for damages including lost profits and additional carrying costs incurred by Johnson due to the breach.
        """,
        "hash": "abc123",
        "timestamp": "2020-03-15T10:30:00Z"
    },
    {
        "id": "002", 
        "title": "Brown v. City of Los Angeles",
        "citation": "789 Cal.App.4th 321 (2021)",
        "docket_number": "21-5678",
        "state": "CA",
        "issuer": "California Court of Appeal",
        "document": """
CALIFORNIA COURT OF APPEAL, SECOND DISTRICT

BROWN v. CITY OF LOS ANGELES

No. 21-5678

CIVIL RIGHTS VIOLATION - FOURTH AMENDMENT

OPINION

This appeal arises from a civil rights lawsuit under 42 U.S.C. § 1983, alleging that the City of Los Angeles and its police officers violated Brown's Fourth Amendment rights during a traffic stop.

PROCEDURAL HISTORY

Brown filed suit in federal district court alleging excessive force and unlawful search and seizure. The district court granted summary judgment in favor of the defendants, finding qualified immunity applied.

FACTS

On June 10, 2020, Los Angeles Police Department officers stopped Brown's vehicle for speeding. During the stop, officers allegedly used excessive force when Brown questioned the basis for the stop. Officers also searched Brown's vehicle without consent or probable cause.

Body camera footage shows Brown was cooperative throughout the encounter. The search yielded no contraband or evidence of criminal activity.

ANALYSIS

The Fourth Amendment protects against unreasonable searches and seizures. A traffic stop constitutes a seizure under the Fourth Amendment and must be justified by reasonable suspicion of criminal activity.

While the initial stop for speeding was justified, the subsequent search of Brown's vehicle lacked probable cause or exigent circumstances. The officers' actions exceeded the scope of a routine traffic stop.

Regarding the excessive force claim, the evidence shows Brown posed no threat and was fully compliant. The use of force was objectively unreasonable under the circumstances.

HOLDING

The district court erred in granting summary judgment. Genuine issues of material fact exist regarding both the unreasonable search and excessive force claims. The officers are not entitled to qualified immunity as the constitutional violations were clearly established.

DISPOSITION

REVERSED and REMANDED for further proceedings consistent with this opinion.
        """,
        "hash": "def456",
        "timestamp": "2021-05-20T14:45:00Z"
    },
    {
        "id": "003",
        "title": "Tech Corp v. Innovation LLC",
        "citation": "456 F.Supp.3d 789 (N.D. Cal. 2022)",
        "docket_number": "22-9012",  
        "state": "CA",
        "issuer": "United States District Court for the Northern District of California",
        "document": """
UNITED STATES DISTRICT COURT
NORTHERN DISTRICT OF CALIFORNIA

TECH CORP v. INNOVATION LLC

Case No. 22-9012

INTELLECTUAL PROPERTY DISPUTE - PATENT INFRINGEMENT

ORDER GRANTING PLAINTIFF'S MOTION FOR PRELIMINARY INJUNCTION

This matter comes before the Court on Plaintiff Tech Corp's motion for a preliminary injunction to prevent Defendant Innovation LLC from continuing to manufacture and sell products that allegedly infringe Tech Corp's patents.

BACKGROUND

Tech Corp holds several patents related to smartphone touchscreen technology, including Patent No. 10,123,456 ("the '456 patent") and Patent No. 10,789,012 ("the '012 patent"). These patents cover methods for multi-touch gesture recognition and haptic feedback systems.

Innovation LLC launched a new smartphone product line in January 2022 that Tech Corp claims incorporates the patented technology without authorization. Tech Corp sent cease and desist letters but Innovation LLC refused to discontinue the allegedly infringing products.

LEGAL STANDARD

To obtain a preliminary injunction, a plaintiff must demonstrate: (1) likelihood of success on the merits; (2) irreparable harm absent an injunction; (3) the balance of hardships favors the plaintiff; and (4) the injunction serves the public interest.

ANALYSIS

Likelihood of Success: Tech Corp has presented substantial evidence that Innovation LLC's products practice the claimed methods in both the '456 and '012 patents. Innovation LLC's invalidity defenses are weak and unlikely to succeed.

Irreparable Harm: Patent infringement typically causes irreparable harm through loss of market share and erosion of licensing opportunities. Tech Corp has demonstrated such harm is occurring and will continue absent an injunction.

Balance of Hardships: While Innovation LLC will face significant costs in redesigning its products, Tech Corp's investment in research and development warrants protection. The hardship to Tech Corp from continued infringement outweighs Innovation LLC's burden.

Public Interest: Protecting valid patent rights serves the public interest by encouraging innovation and investment in research and development.

CONCLUSION

All four factors for preliminary injunctive relief are satisfied. Tech Corp's motion is GRANTED. Innovation LLC is enjoined from manufacturing, selling, or distributing products that infringe the '456 and '012 patents pending final resolution of this case.

IT IS SO ORDERED.
        """,
        "hash": "ghi789",
        "timestamp": "2022-08-12T16:20:00Z"
    }
]

def get_mock_dataset():
    """Return mock dataset for development"""
    return MOCK_LEGAL_DOCS