enWords = document.querySelectorAll('.TermText.notranslate.lang-en');
enList = "";
console.log("English-List");
for(en of enWords){
	enList += en.innerText + "\n";
}
console.log(enList);

viWords = document.querySelectorAll('.TermText.notranslate.lang-vi');
viList = "";
console.log("VietNam-List");
for(vi of viWords){
	viList += vi.innerText + "\n";
}
console.log(viList);