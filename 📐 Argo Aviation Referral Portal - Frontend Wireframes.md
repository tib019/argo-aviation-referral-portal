# Argo Aviation Referral Portal - Frontend Wireframes

## Übersicht

Diese Wireframes definieren die komplette Benutzeroberfläche für das Argo Aviation Referral Portal MVP. Basierend auf der bestehenden Authentifizierung (Login, Register, Dashboard) werden hier alle verbleibenden Frontend-Komponenten spezifiziert.

---

## **1. Job Listings Seite**

### **Layout-Struktur:**
```

 [️ Argo Aviation] [Dashboard] [Meine Referrals] [Profil] [Logout]


 Aktuelle Stellenausschreibungen


 [ Suche] [ Standort] [ Bereich]



 Senior Software Engineer
 München • €70.000-90.000 • Vollzeit
 Referral Bonus: €2.500

 Wir suchen einen erfahrenen Software Engineer...
 [ Details anzeigen] [ Kandidat empfehlen]



 Marketing Manager
 Berlin • €55.000-70.000 • Vollzeit
 Referral Bonus: €1.800

 Für unser Marketing-Team suchen wir...
 [ Details anzeigen] [ Kandidat empfehlen]


 [ Vorherige] [1] [2] [3] [4] [5] [Nächste ]


```

### **Funktionale Spezifikationen:**
- **Suchfilter:** Echtzeit-Suche nach Jobtitel, Skills, Standort
- **Sortierung:** Nach Datum, Gehalt, Referral-Bonus
- **Pagination:** 10 Jobs pro Seite
- **Responsive:** Mobile-optimierte Karten-Ansicht
- **Call-to-Action:** Prominente "Kandidat empfehlen" Buttons

---

## **2. Job Detail Seite**

### **Layout-Struktur:**
```

 [️ Argo Aviation] [Dashboard] [Jobs] [Meine Referrals] [Logout]


 ← Zurück zu Jobs


 Senior Software Engineer
 Argo Aviation GmbH



 München €70-90k Vollzeit



 Referral Bonus: €2.500
 Veröffentlicht: 15.08.2025
 Bewerbungsfrist: 15.09.2025


 Stellenbeschreibung

 Als Senior Software Engineer entwickeln Sie innovative...
 [Vollständige Beschreibung]

 Anforderungen

 • 5+ Jahre Erfahrung in Python/JavaScript
 • Erfahrung mit Cloud-Technologien (Azure/AWS)
 • Teamführung und Mentoring

 Benefits

 • Flexible Arbeitszeiten • Home Office • Weiterbildung


 [ KANDIDAT EMPFEHLEN]



```

### **Funktionale Spezifikationen:**
- **Vollständige Job-Details:** Beschreibung, Anforderungen, Benefits
- **Referral-Informationen:** Bonus-Höhe, Bedingungen
- **Social Sharing:** LinkedIn, E-Mail teilen
- **Bookmark-Funktion:** Job für später speichern

---

## **3. Referral Submission Formular**

### **Layout-Struktur:**
```

 [️ Argo Aviation] [Dashboard] [Jobs] [Meine Referrals] [Logout]


 Kandidat empfehlen


 Position: Senior Software Engineer
 Referral Bonus: €2.500


 Kandidaten-Informationen


 [Vorname*] [Nachname*]



 [E-Mail-Adresse*]



 [Telefonnummer]



 [LinkedIn Profil URL]


 Lebenslauf hochladen

 [ Datei auswählen] [Keine Datei]


 Warum empfehlen Sie diesen Kandidaten?

 [Beschreiben Sie die Qualifikationen und warum der
 Kandidat für diese Position geeignet ist...]




 Beziehung zum Kandidaten

 [ Kollege/Ex-Kollege]


 ️ Ich bestätige, dass der Kandidat über diese Empfehlung
 informiert ist und der Kontaktaufnahme zustimmt


 [ EMPFEHLUNG SENDEN]



```

### **Funktionale Spezifikationen:**
- **Validierung:** Pflichtfelder, E-Mail-Format, Datei-Upload
- **Datei-Upload:** PDF/DOC Lebenslauf, max. 5MB
- **Dropdown-Optionen:** Beziehungstypen (Kollege, Freund, etc.)
- **Bestätigungen:** DSGVO-konforme Einverständniserklärungen

---

## **4. Meine Referrals Dashboard**

### **Layout-Struktur:**
```

 [️ Argo Aviation] [Dashboard] [Jobs] [Meine Referrals] [Logout]


 Meine Referrals


 Gesamt Pending Erfolg Verdient
 12 5 3 €7.500



 [ Suche] [ Zeitraum] [ Status]



 Max Mustermann
 Senior Software Engineer • 15.08.2025
 Status: Interview geplant • Bonus: €2.500

 Nächster Schritt: Interview am 20.08.2025
 [ Details] [️ Notiz hinzufügen] [ Nachfragen]



 Anna Schmidt
 Marketing Manager • 10.08.2025
 Status: Eingestellt • Bonus: €1.800 (ausstehend)

 Gratulation! Bonus wird in 30 Tagen ausgezahlt.
 [ Details] [ Teilen] [ Bonus-Info]



 Tom Weber
 DevOps Engineer • 05.08.2025
 Status: Abgelehnt • Bonus: €0

 Grund: Qualifikationen nicht passend
 [ Details] [ Feedback] [ Tipps]



```

### **Funktionale Spezifikationen:**
- **Status-Tracking:** Echtzeit-Updates über Bewerbungsstatus
- **Statistiken:** Übersichtliche KPIs und Erfolgsmetriken
- **Filterung:** Nach Status, Zeitraum, Position
- **Aktionen:** Notizen, Nachfragen, Teilen von Erfolgen

---

## **5. Referrer Profil Seite**

### **Layout-Struktur:**
```

 [️ Argo Aviation] [Dashboard] [Jobs] [Meine Referrals] [Logout]


 Mein Profil


 [Profilbild] Tobias Helko Buß
 Superadmin
 tobi196183@gmail.com
 +49 123 456789
 Mitglied seit: August 2025
 [️ Bearbeiten]


 Meine Statistiken

 Referrals Erfolg Verdient Rang
 12 25% €7.500 Gold


 Spezialisierungen

 [ IT & Software] [ Marketing] [ Engineering]
 [ Management] [ Design] [+ Hinzufügen]


 Netzwerk & Kontakte

 LinkedIn: linkedin.com/in/tobias-buss
 Twitter: @tobias_buss
 Website: tobias-buss.dev
 [️ Bearbeiten]


 Erfolge & Badges

 Erste Empfehlung 5 Referrals €5k verdient
 Top Performer Qualitäts-Referrer


 ️ Einstellungen

 E-Mail-Benachrichtigungen [ An]
 Push-Benachrichtigungen [ Aus]
 Profil-Sichtbarkeit [ Öffentlich]
 Zahlungsinformationen [ Bearbeiten]



```

### **Funktionale Spezifikationen:**
- **Profilbild-Upload:** Drag & Drop, Crop-Funktion
- **Spezialisierungen:** Tag-System für Expertise-Bereiche
- **Social Links:** Integration mit LinkedIn, Twitter
- **Gamification:** Badges, Rang-System, Erfolgs-Tracking

---

## **6. Superadmin Panel (nur für tobi196183@gmail.com)**

### **Layout-Struktur:**
```

 [️ Argo Aviation] [ ADMIN PANEL] [Dashboard] [Logout]


 Superadmin Control Panel


 Benutzer Jobs Referrals Zahlungen
 47 23 156 €45.600


 System-Übersicht

 [ Benutzerverwaltung] [ Job-Management]
 [ Referral-Übersicht] [ Zahlungs-Management]
 [ Analytics & Berichte] [️ System-Einstellungen]
 [ Zoho ATS Integration] [ E-Mail-Templates]


 Aktuelle Warnungen

 ️ 3 Referrals warten auf Genehmigung
 5 Zahlungen sind fällig
 2 E-Mail-Bounces in den letzten 24h


 Letzte Aktivitäten

 Neuer Benutzer: Anna Schmidt (vor 2h)
 Job erstellt: DevOps Engineer (vor 4h)
 Referral eingereicht: Max M. → Software Engineer
 Zahlung verarbeitet: €2.500 an Tom Weber


 Schnellaktionen

 [ Neuen Job erstellen] [ Benutzer hinzufügen]
 [ Bericht generieren] [ Zahlung verarbeiten]
 [ Broadcast senden] [ System-Backup]



```

### **Funktionale Spezifikationen:**
- **Echtzeit-Dashboard:** Live-Updates von System-Metriken
- **Bulk-Aktionen:** Mehrere Datensätze gleichzeitig bearbeiten
- **Audit-Log:** Vollständige Nachverfolgung aller Admin-Aktionen
- **Backup & Recovery:** Automatisierte System-Sicherungen

---

## **7. Mobile Responsive Anpassungen**

### **Smartphone Layout (320px-768px):**
```

 [] Argo Aviation


 Jobs (23)


 [ Suche...]



 Software Eng
 München
 €70-90k
 €2.500 Bonus
 [Details] []



 Marketing
 Berlin
 €55-70k
 €1.800 Bonus
 [Details] []


 [] [1][2][3] []


```

### **Tablet Layout (768px-1024px):**
```

 [️ Argo Aviation] [ Menu] [Profile]


 Stellenausschreibungen


 [ Suche] [ Filter]



 Software Eng Marketing
 München Berlin
 €70-90k €55-70k
 €2.500 €1.800
 [Details][] [Details][]



```

---

## **Design-System Spezifikationen**

### **Farbpalette:**
color--primary: #f6bb41;
color--secondary: #ECC94B;
black: #000000;
cyan-bluish-gray: #abb8c3;
white: #ffffff;
pale-pink: #f78da7;
vivid-red: #cf2e2e;
luminous-vivid-orange: #ff6900;
luminous-vivid-amber: #fcb900;
light-green-cyan: #7bdcb5;
vivid-green-cyan: #00d084;
pale-cyan-blue: #8ed1fc;
vivid-cyan-blue: #0693e3;
vivid-purple: #9b51e0;
gray: #333333;
gray-light: #f6f6f6;

### **Typografie:**
- **Headlines:** Segoe UI, 24-36px, Bold
- **Body Text:** Segoe UI, 16px, Regular
- **Captions:** Segoe UI, 14px, Medium

### **Spacing:**
- **Margins:** 8px, 16px, 24px, 32px
- **Padding:** 12px, 16px, 20px, 24px
- **Border Radius:** 8px, 12px, 16px

### **Komponenten:**
- **Buttons:** Gradient backgrounds, hover animations
- **Cards:** Subtle shadows, rounded corners
- **Forms:** Focus states, validation feedback
- **Navigation:** Sticky header, breadcrumbs

---

## **Interaktions-Spezifikationen**

### **Hover-Effekte:**
- **Buttons:** Transform scale(1.02), shadow increase
- **Cards:** Lift effect with shadow
- **Links:** Color transition, underline animation

### **Loading-States:**
- **Skeleton Screens:** Für Job-Listen und Referral-Übersichten
- **Progress Indicators:** Für Datei-Uploads und Form-Submissions
- **Spinner:** Für API-Calls und Datenladung

### **Micro-Animations:**
- **Success Feedback:** Checkmark animation bei erfolgreichen Aktionen
- **Error Shake:** Subtle shake bei Validierungsfehlern
- **Slide Transitions:** Zwischen Seiten und Modals

---

## **Performance-Anforderungen**

### **Ladezeiten:**
- **Initial Page Load:** < 2 Sekunden
- **Navigation:** < 500ms
- **Search Results:** < 1 Sekunde
- **Form Submission:** < 3 Sekunden

### **Accessibility (WCAG 2.1 AA):**
- **Keyboard Navigation:** Vollständig navigierbar
- **Screen Reader:** Semantische HTML-Struktur
- **Color Contrast:** Mindestens 4.5:1 Ratio
- **Focus Indicators:** Deutlich sichtbare Focus-States

---

## **Nächste Implementierungsschritte**

1. **Job Listings Seite** (Priorität: Hoch)
2. **Referral Submission Formular** (Priorität: Hoch)
3. **Meine Referrals Dashboard** (Priorität: Mittel)
4. **Referrer Profil Seite** (Priorität: Mittel)
5. **Superadmin Panel** (Priorität: Niedrig)
6. **Mobile Optimierungen** (Priorität: Hoch)

Diese Wireframes bilden die Grundlage für die vollständige Frontend-Implementierung des Argo Aviation Referral Portals.

