=================================================
QA / SDET Interview Script
=================================================

-------------------------------------------------
Integration / Unit Testing
-------------------------------------------------

Give an example service and ask for the candidate to write
unit or integration tests in the language they are most comfortable
with::

    public class Contact {
        public string Name { get; set; }
        public string Email { get; set; }
        public string PhoneNumber { get; set; } 
    }

    public interface AddressBook {
        public List<Contact> getContacts(string customerId);
        public void addContact(string customerId, Contact contact)
    }

-------------------------------------------------
Automated Testing
-------------------------------------------------

* Can they generate a test plan given design documents
  - what parts of the system will they test (input/output)
  - can they generate tests based on user stories

* How would they design a continuous deployment system
  - push to source control
  - run unit tests, lint tests, style tests, etc
  - deploy to white room isolated environment
  - run integration tests, validation tests
  - automatically build release
  - deploy to production
  - run final smoke tests, performance tests
  - automated roll-back

-------------------------------------------------
Frontend Testing
-------------------------------------------------

* do they have experience with automated GUI testing
  - selenium
  - phantomJS
  - UI scripting
  - I18N Testing
  - cross browser diffing

* do they have experience with internationalization
* do they have experience testing devices (and sizes)
  - android
  - ios
  - tablets
  - custom

-------------------------------------------------
Security Testing
-------------------------------------------------

* do they know about common HTTP vulnerabilities
  - sql injection
  - cookie injection
  - session injection
  - information leakage
* do they have experience fuzzing
* do they have experience using man in the middle tools
  - fiddler
  - wireshark
* do they have experience with automated penetration test tools
  - burp suite
  - metasploit
* do they have experience with code scanners
  - forify
  - any lint tools
  - any complexity scanning tools