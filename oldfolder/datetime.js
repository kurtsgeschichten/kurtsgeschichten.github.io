function berechne() {
    var jetzt = new Date(),
    tag = jetzt.getDate(),
    tagZahl = jetzt.getDay(),
    wochentag = ['Sonntag','Montag','Dienstag','Mittwoch','Donnerstag','Freitag','Samstag' ],
    monatZahl = jetzt.getMonth(),
    monat = ['Januar','Februar','März','April','Mai','Juni','Juli','August','September',    
            'Oktober','November','Dezember'],
    text;
    text = tag + '. ' + monat[monatZahl];
    document.getElementById('datetime').innerHTML = text;	
}
berechne();
