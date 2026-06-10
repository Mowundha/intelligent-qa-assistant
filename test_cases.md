# Test Cases Log

## In-Scope Queries (Questions the system can answer)

### Test Case 1
**Query:** How do I check my account balance?
**Expected:** System returns answer from banking documents
**Actual:** "You can check your account balance through internet banking, mobile app, ATM, or by visiting your nearest branch."
**Sources Used:** 3 chunks from account_faq.txt
**Result:** ✅ PASS

---

### Test Case 2
**Query:** How do I block my debit card?
**Expected:** System returns card blocking instructions
**Actual:** "You can block your debit card immediately through mobile banking app, internet banking, or by calling customer care."
**Sources Used:** 3 chunks from cards_faq.txt
**Result:** ✅ PASS

---

### Test Case 3
**Query:** What documents are needed for a car loan?
**Expected:** System returns required documents list
**Actual:** "For car loan you need ID proof, address proof, income proof, bank statements of last 6 months and car quotation."
**Sources Used:** 3 chunks from loans_faq.txt
**Result:** ✅ PASS

---

## Out-of-Scope Queries (System must return "I don't know")

### Test Case 4
**Query:** Who won IPL 2024?
**Expected:** System returns "I don't know"
**Actual:** "I don't know"
**Result:** ✅ PASS

---

### Test Case 5
**Query:** Tell me a joke
**Expected:** System returns "I don't know"
**Actual:** "I don't know"
**Result:** ✅ PASS

---

### Test Case 6
**Query:** What is the capital of France?
**Expected:** System returns "I don't know"
**Actual:** "I don't know"
**Result:** ✅ PASS

---

## Edge Cases

### Test Case 7
**Query:** (empty string)
**Expected:** System shows warning message
**Actual:** "Please enter a question!" warning displayed
**Result:** ✅ PASS

---

### Test Case 8
**Query:** asdfjkl qwerty zxcvbn
**Expected:** System returns "I don't know" — gibberish query
**Actual:** "I don't know"
**Result:** ✅ PASS

---

### Test Case 9
**Query:** How do I reset my internet banking password?
**Expected:** System returns password reset instructions
**Actual:** "You can reset your password through forgot password option on internet banking portal using your registered mobile number."
**Sources Used:** 3 chunks from general_banking_faq.txt
**Result:** ✅ PASS

---

### Test Case 10
**Query:** What is KYC?
**Expected:** System explains KYC from documents
**Actual:** "KYC stands for Know Your Customer. It is a mandatory process to verify customer identity as per RBI regulations."
**Sources Used:** 3 chunks from general_banking_faq.txt
**Result:** ✅ PASS

