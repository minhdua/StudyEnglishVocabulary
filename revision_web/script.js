// Data
function checkInput(value) {
  return /^\d+((\-?\d+(\;|$)|\!\d+(\;|$)|\;)\d*)*$/.test(value); 
}

function showError(message){
	error = $('#error');
	error.html(message);
	if(error.hasClass('hidden')){
		error.toggleClass('hidden');
	}
}
function removeError(){
	error = $('#error');
	error.html("");
	if(!error.hasClass('hidden')){
		error.toggleClass('hidden');
	}
}
function setInputFilter(textbox, inputFilter) {
  ["input", "keydown", "keyup", "mousedown", "mouseup", "select", "contextmenu", "drop"].forEach(function(event) {
    textbox.addEventListener(event, function() {
      if (inputFilter(this.value)) {
        this.oldValue = this.value;
        this.oldSelectionStart = this.selectionStart;
        this.oldSelectionEnd = this.selectionEnd;
      } else if (this.hasOwnProperty("oldValue")) {
        this.value = this.oldValue;
        this.setSelectionRange(this.oldSelectionStart, this.oldSelectionEnd);
      } else {
        this.value = "";
      }
    });
  });
}
var current_choices = [];
var current_choice = 0;
var synth = window.speechSynthesis;
var rightTimes = 0;
var wrongTimes = 0;
var wrongList = "";
function setResult(){
	$('#Right-times').text(rightTimes);
	$('#Wrong-times').text(wrongTimes);
	$('#Wrong-words-list').html('');
	$('#Wrong-words-list').append(wrongList);
}
$(document).ready(function(){
	setInputFilter(document.getElementById("range-box"), function(value) {
		return /^\d*((\-|\;|\!)?\d*)*$/.test(value); // Allow digits and '.' only, using a RegExp
	});
	$('#submit-button').click(function(){
		removeError();
		value = $('#range-box').val();
		choice_list = [];
		if(checkInput(value)){
			if(value.endsWith('-0')){
				value += words.length;
			}
			choices = value.split(';');
			for(choice of choices){
				if(choice.includes('-')){
					chs = choice.split('-');
					a = parseInt(chs[0]);
					b = parseInt(chs[1]);
					for(i=a;i<=b;i++){
						choice_list.push(i-1);
					}
				}else{
					if(choice.includes('!')){
						chs = choice.split('!');
						c = parseInt(chs[1]);
						choice_list = choice_list.filter(function(value, index, arr){ 
							return value !== c-1;
						});
					}else{
						if(choice !== ''){
							d = parseInt(choice);
							choice_list.push(d-1);
						}
					}
				}
			}
			choice_list = [...new Set(choice_list)];
			
		}else{
			message = 'using "-" between two number to choose from xth to yth choice. <br/>'
					+ 'using ";" between to separate 2 choices.<br/>'
					+ 'using "!" before to not choose 1 choice.<br/>'
					+ 'Example: 1-5;10;15;20-25;!23 => 1,2,3,4,5,10,15,20,21,22,24,25';
			showError(message);
		}
		word_list = [];
		for(choice of choice_list){
			if(choice < words.length){
				word_list.push(words[choice]);
			}
		}
		current_choices = [word_list];
		
		createTable(word_list);
		if(!$('.revision-mode .dash .arrow-right').hasClass('hidden')){
			$('.revision-mode .dash .arrow-right').click();
		}
	});
	
	$('#random-button').click(function(){
		var shuffle_choices  = [...current_choices].sort((a, b) => 0.5 - Math.random());
		createTable(shuffle_choices);
	});
	
	$('.arrow-right').click(function(){
		if(current_choices.length>0){
			showInfor();
			setResult();
			cover = $(this).parent().parent().find('.cover');
			arrowDown = $(this).parent().parent().find('.arrow-down');
			cover.toggleClass('hidden');
			arrowDown.toggleClass('hidden');
			$(this).toggleClass('hidden');
		}
	});
	$('#speech').click(function(){
		speakWord(current_choices[current_choice].english);
	});
	
	$('.arrow-down').click(function(){
		cover = $(this).parent().parent().find('.cover');
		arrowDown = $(this).parent().parent().find('.arrow-right');
		cover.toggleClass('hidden');
		arrowDown.toggleClass('hidden');
		$(this).toggleClass('hidden');
	});
	
	$('#Pre-button').click(function(){
		if(current_choice>0){
			current_choice -= 1;
		}
		showInfor();
	});
	
	$('#Next-button').click(function(){
		if(current_choice <current_choices.length-1){
			current_choice += 1;
		}
		showInfor();
	});
	
	$("#practice-input").on('keyup', function (e) {
		if (e.key === 'Enter' || e.keyCode === 13) {
			value = $("#practice-input").val().toLowerCase();
			english = current_choices[current_choice].english.toLowerCase();
			if(value === english){
				if($('#Auto-next').prop('checked')){
					$('#Next-button').click();
				}
				rightTimes += 1;
			}else{
				wrongTimes += 1;
				wrongWords = wrongList.split("; ");
				if(!wrongWords.includes(value)){
					word = compareWord(value,english);
					
					if(wrongWords[0] !== ''){
						wrongList += '; ' + word;
					}
					else{
						wrongList += word;
					}
				}
			}
			
			if($('#Speaker').prop('checked')){
					$('#speech').click();
			}
			$("#practice-input").val('');
			setResult();
		}
		
	});
	$('#hidden-english-revise-button').click(function(){
		hidenEnglish();
	});
	$('#show-english-revise-button').click(function(){
		showEnglish();
	});	
	$('#checkall-english-revise-button').click(function(){
		rows = getCheckedRow().find('.checker');
		for(row of rows){
			$(row).click();
		}
	});
	$('#clear-english-revise-button').click(function(){
		clearAllEnglish();
	});
	
	$('#hidden-vietnamese-revise-button').click(function(){
		hidenVietNamese();
	});
	$('#show-vietnamese-revise-button').click(function(){
		showVietNamese();
	});
	$('#checkall-vietnamese-revise-button').click(function(){
		rows = getCheckedRow().find('.checker');
		for(row of rows){
			$(row).click();
		}
	});
	
	$('#clear-vietnamese-revise-button').click(function(){
		clearAllVietNamese();
	});
	$("#range-box").on('keyup', function (e) {
		if (e.key === 'Enter' || e.keyCode === 13) {
			$('#submit-button').click();
		}
	});
	
});
function compareWord(value,english){
	sameIdValue = longestCommonSubsequence(value,english).split(' ').filter((value,index,arr) =>{
		return value !== '';
	});
	sameIdEnglish = longestCommonSubsequence(english,value).split(' ').filter((value,index,arr) =>{
		return value !== '';
	});
	console.log('value: '+sameIdValue);
	console.log('english: '+sameIdEnglish);
	word = '';
	var i;
	idEndValue =  parseInt(sameIdValue[0]);
	idEndEnglish =  parseInt(sameIdEnglish[0]);
	word += '<span class="cross">'+value.substring(0,idEndValue)+'</span>';
	word += '<ins class="gray">'+english.substring(0,idEndEnglish)+'</ins>';
	for( i = 0; i < sameIdValue.length; i ++ ){
		idEnglish =  parseInt(sameIdEnglish[i]);
		idValue =  parseInt(sameIdValue[i]);
		if(i>0){
			idStartValue =  parseInt(sameIdValue[i-1])+1;
			idEndValue =  parseInt(sameIdValue[i]);
			idStartEnglish =  parseInt(sameIdEnglish[i-1])+1;
			idEndEnglish =  parseInt(sameIdEnglish[i]);
			distanceValue = idEndValue - idStartValue;
			distanceEnglish = idEndEnglish - idStartEnglish;
			word += '<span class="cross">'+value.substring(idStartValue,idStartValue+distanceValue)+'</span>';
			word += '<ins class="gray">'+english.substring(idStartEnglish,idStartEnglish+distanceEnglish)+'</ins>';
		}
		word += value[idValue];
		//console.log('word '+word);
	}
	startEnglish = parseInt(sameIdEnglish[i-1])+1;
	startValue = parseInt(sameIdValue[i-1])+1;
	word += '<span class="cross">'+value.substring(startValue)+'</span>';
	word += '<ins class="gray">'+english.substring(startEnglish)+'</ins>';
	return word;
}
function checkEnglish(){
	
	
}

function checkVietName(){
	
}
function getAllRow(){
	return $('.display-row');
}

function checkedAll(){
	checkboxs = getAllRow().find('input[type=checkbox]');
	checkboxs.prop('checked',true);
}
function unCheckedAll(){
	checkboxs = getAllRow().find('input[type=checkbox]');
	checkboxs.prop('checked',false);
}

function max(a,b){
	if (a > b) return a;
	return b;
}
function sharedStart(array){
    var A= array.concat().sort(), 
    a1= A[0], a2= A[A.length-1], L= a1.length, i= 0;
    while(i<L && a1.charAt(i)=== a2.charAt(i)) i++;
    return i;
}

function speakWord(word){
	var utterThis = new SpeechSynthesisUtterance(word);
	utterThis.rate = 0.75;
	utterThis.voice = synth.getVoices()[3];
	utterThis.lang = 'en-US';
	synth.speak(utterThis);
}
function showInfor(){
	var current_word = current_choices[current_choice];
	$('#No-info').text(current_word.no);
	$('#English-info').text(current_word.english);
	$('#Vietnamese-info').text(current_word.vietnamese);
	$('#Pronounce-info').text(current_word.pronoun);
}
// create table
function getRow(){
	return $('.display-row').length;
}
function createTable(datas){
	current_choices = datas;
	// get table
	table = $('#data-table');
	// delete all innerHTML
	table.html("");
	rowNumber = getRow()+1;
	// add new row
	// add new col
	table.append('\
		<tr id="0">\
			<th class ="cell">\
				<button id="no-button">No.</button>\
			</th>\
			<th class ="cell">\
				<input id="checkall" type="checkbox"></input>\
			</th>\
			<th class ="cell">\
				English\
			</th>\
			<th class ="cell">\
				Vietnamese\
			</th>\
			<th class ="cell">\
				Pronounce\
			</th>\
			<th class ="cell">\
				Speaker\
			</th>\
			<th class ="cell">\
				Browser\
			</th>\
			<th class ="cell hidden">\
				Check\
			</th>\
		<tr>\
	');
	$('#no-button').click(function(){
		$('.no-word').toggleClass('hidden');
		$('.no-row').toggleClass('hidden');
	});
	$('#checkall').click(function(){
		if($(this).is(':checked')) checkedAll();
		else unCheckedAll();
	});
	for(data of datas){
		table.append('\
			<tr class="hidden-row hidden" id ="'+rowNumber+'h"> \
				<td class="error-row" colspan="8">\
				This is a error\
				</td>\
			</tr>\
			<tr class="display-row" id ="'+rowNumber+'">\
				<td class ="cell">\
					<span class="no-word hidden">'+data.no+'</span>\
					<span class="no-row">'+rowNumber+'</span>\
				</td>\
				<td class ="cell">\
					<input type="checkbox"></input>\
				</td>\
				<td class ="cell">\
					<span class="english-word">'+data.english+'</span>\
					<input type="text" class="english-word hidden"/>\
				</td>\
				<td class ="cell">\
					<span class="vietnamese-word">'+data.vietnamese+'</span>\
					<input type="text" class="vietnamese-word hidden"/>\
				</td>\
				<td class ="cell">\
					'+data.pronounce+'\
				</td>\
				<td class ="cell">\
					<button class ="center speaker">\
					<svg  xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-megaphone-fill" viewBox="0 0 16 16">\
					  <path d="M13 2.5a1.5 1.5 0 0 1 3 0v11a1.5 1.5 0 0 1-3 0v-11zm-1 .724c-2.067.95-4.539 1.481-7 1.656v6.237a25.222 25.222 0 0 1 1.088.085c2.053.204 4.038.668 5.912 1.56V3.224zm-8 7.841V4.934c-.68.027-1.399.043-2.008.053A2.02 2.02 0 0 0 0 7v2c0 1.106.896 1.996 1.994 2.009a68.14 68.14 0 0 1 .496.008 64 64 0 0 1 1.51.048zm1.39 1.081c.285.021.569.047.85.078l.253 1.69a1 1 0 0 1-.983 1.187h-.548a1 1 0 0 1-.916-.599l-1.314-2.48a65.81 65.81 0 0 1 1.692.064c.327.017.65.037.966.06z"/>\
					</svg>\
					</button>\
				</td>\
				<td class ="cell">\
					<button class ="center browser">\
					<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-search" viewBox="0 0 16 16">\
					  <path d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001c.03.04.062.078.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1.007 1.007 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0z"/>\
					</svg>\
					</button>\
				</td>\
				<td class ="cell hidden">\
					<button class ="center checker">\
						<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-patch-check-fill" viewBox="0 0 16 16">\
						  <path d="M10.067.87a2.89 2.89 0 0 0-4.134 0l-.622.638-.89-.011a2.89 2.89 0 0 0-2.924 2.924l.01.89-.636.622a2.89 2.89 0 0 0 0 4.134l.637.622-.011.89a2.89 2.89 0 0 0 2.924 2.924l.89-.01.622.636a2.89 2.89 0 0 0 4.134 0l.622-.637.89.011a2.89 2.89 0 0 0 2.924-2.924l-.01-.89.636-.622a2.89 2.89 0 0 0 0-4.134l-.637-.622.011-.89a2.89 2.89 0 0 0-2.924-2.924l-.89.01-.622-.636zm.287 5.984-3 3a.5.5 0 0 1-.708 0l-1.5-1.5a.5.5 0 1 1 .708-.708L7 8.793l2.646-2.647a.5.5 0 0 1 .708.708z"/>\
						</svg>\
					</button>\
				</td>\
				<td class="cell">\
					<input type="textbox" class="study-word">\
					</input>\
				</td>\
			</tr>\
		');
		$('#'+rowNumber+' input.english-word').on('keyup', function (e) {
			if (e.keyCode == '38') {
				 // up arrow
				id = $(this).parents('.display-row').get(0).id;
				console.log('up'+id);
				moveUp(id,'english');
			}
			else if (e.keyCode == '40' || e.key === 'Enter' || e.keyCode === 13) {
				if(e.altKey){
					$(this).parents('.display-row').find('.checker').click();
					$(this).parents('.display-row').find('.speaker').click();
				}
				if(e.ctrlKey){
					$('#checkall-english-revise-button').click();
				}
				// down arrow
				id = $(this).parents('.display-row').get(0).id;
				console.log('down'+id);
				moveDown(id,'english');
			} 
			if(this.value.length >20){
				this.style.width = ((this.value.length + 1) * 8) + 'px';
			}else{
				this.style.width ='180px';
			}
		});
		$('#'+rowNumber+' input.vietnamese-word').on('keyup', function (e) {
			
			if (e.keyCode == '38') {
				 // up arrow
				id = $(this).parents('.display-row').get(0).id;
				console.log('up'+id);
				moveUp(id,'vietnamese');
			}
			else if (e.keyCode == '40' || e.key === 'Enter' || e.keyCode === 13) {
				if(e.altKey){
					$(this).parents('.display-row').find('.checker').click();
				}
				if(e.ctrlKey){
					$('#checkall-vietnamese-revise-button').click();
				}
				// down arrow
				id = $(this).parents('.display-row').get(0).id;
				console.log('down'+id);
				moveDown(id,'vietnamese');
			}
			
			if(this.value.length >20){
				this.style.width = ((this.value.length + 1) * 8) + 'px';
			}else{
				this.style.width ='180px';
			}
		});
		$('#'+rowNumber+' .study-word').on('keyup', function (e) {
			if (e.key === 'Enter' || e.keyCode === 13) {
				origin = $(this).parents('.display-row').find('span.english-word').text();
				english = origin.toLowerCase();
				value = $(this).val().toLowerCase();
				if(english === value){
					speakWord(english);
					$(this).val('');
				}else{
					speakWord('Wrong');
				}
			}else{
				if (e.keyCode == '38'){
					id = $(this).parents('.display-row').get(0).id;
					console.log('up'+id);
					moveUp(id,'study');
				}else{
					 if (e.keyCode == '40'){
						 id = $(this).parents('.display-row').get(0).id;
						console.log('up'+id);
						moveDown(id,'study');
					 }
				}
			}
			
		});
		$('#'+rowNumber+' .speaker').click(function(){
			speakWord($(this).parents('.display-row').find('.english-word').text());
		});
		$('#'+rowNumber+' .browser').click(function(){
			gotoWord($(this).parents('.display-row').find('.english-word').text());
		});
		$('#'+rowNumber+' .checker').click(function(){
			if(checkMode == 1){
				var origin = $(this).parents('.display-row').find('span.english-word').text();
				var english = origin.toLowerCase();
				var input_tag = $(this).parents('.display-row').find('input.english-word');
				var value = input_tag.val().toLowerCase();
				var id = '#'+$(this).parents('.display-row').get(0).id+'h';
				if(value === english){
					if(input_tag.hasClass('errorVal')){
						input_tag.toggleClass('errorVal');
					}
					showRowMessage(id,'<span class="green">OK:'+origin+'</span>')
				}else{
					if(!input_tag.hasClass('errorVal')){
						input_tag.toggleClass('errorVal');
					}
					word = compareWord(value,english);
					showRowMessage(id,'<span class="red">Wrong: </span>'+word);
				}
			}else{
				origin = $(this).parents('.display-row').find('span.vietnamese-word').text();
				vietnamese = origin.toLowerCase();
				input_tag = $(this).parents('.display-row').find('input.vietnamese-word');
				value = input_tag.val().toLowerCase();
				id = '#'+$(this).parents('.display-row').get(0).id+'h';
				if(value === vietnamese){
					if(input_tag.hasClass('errorVal')){
						input_tag.toggleClass('errorVal');
					}
					showRowMessage(id,'<span class="green">OK:'+origin+'</span>')
				}else{
					if(!input_tag.hasClass('errorVal')){
						input_tag.toggleClass('errorVal');
					}
					word = compareWord(value,vietnamese);
					showRowMessage(id,'<span class="red">Wrong: </span>'+word);
				}
			}
		});
		rowNumber += 1;
	}
	$('#hidden-english-revise-button').prop('disabled',false);
	$('#show-english-revise-button').prop('disabled',false);
	$('#checkall-english-revise-button').prop('disabled',true);
	$('#clear-english-revise-button').prop('disabled',true);
	
	$('#hidden-vietnamese-revise-button').prop('disabled',false);
	$('#show-vietnamese-revise-button').prop('disabled',false);
	$('#checkall-vietnamese-revise-button').prop('disabled',true);
	$('#clear-vietnamese-revise-button').prop('disabled',true);
	
}

function moveUp(id,type){
	if(id > 1){
		idUp = parseInt(id)-1;
		while(idUp > 1){
			input = $('#'+idUp+' input.'+type+'-word');
			if(input.hasClass('hidden')){
				idUp -- ;
			}else{
				break;
			}
		}
		$('#'+idUp+' input.'+type+'-word').focus();
	}
}

function moveDown(id,type){
	if(id < current_choices){
		idDown = parseInt(id)+1;
		while(idDown > 1){
			input = $('#'+idDown+' input.'+type+'-word');
			if(input.hasClass('hidden')){
				idDown ++ ;
			}else{
				break;
			}
		}
		$('#'+idDown+' input.'+type+'-word').focus();
	}
}
function clearAllEnglish(){
	rowsInput = getCheckedRow().find('input.english-word');
	for(row of rowsInput){
		$(row).val('');
	}
}
function clearAllVietNamese(){
	rowsInput = getCheckedRow().find('input.vietnamese-word');
	for(row of rowsInput){
		$(row).val('');
	}
}
function showRowMessage(id,message){
	$(id).find('.error-row').html('');
	$(id).find('.error-row').append(message);
	if($(id).hasClass('hidden')){
		$(id).toggleClass('hidden');
	}
}
function hiddenAllRowMessage(){
	rowsError = $('.error-row');
	for(row of rowsError){
		if(!$(row).parent().hasClass('hidden')){
			$(row).parent().toggleClass('hidden');
		}
	}
}
function getCheckedRow(){
	return $('.display-row input:checked').parents('.display-row');
}
var checkMode = 0;
function hidenEnglish(){
	rowsSpan = getCheckedRow().find('span.english-word');
	rowsInput = getCheckedRow().find('input.english-word');
	rowsCheck = getCheckedRow().find('.checker').parent();
	for(row of rowsSpan){
		if(!$(row).hasClass('hidden')){
			$(row).toggleClass('hidden');
		}
	}
	for(row of rowsInput){
		if($(row).hasClass('hidden')){
			$(row).toggleClass('hidden');
		}
	}
	
	for(row of rowsCheck){
		if($(row).hasClass('hidden')){
			$(row).toggleClass('hidden');
		}
	}
	$('#hidden-vietnamese-revise-button').prop('disabled',true);
	$('#show-vietnamese-revise-button').prop('disabled',true);
	$('#checkall-vietnamese-revise-button').prop('disabled',true);
	
	$('#checkall-english-revise-button').prop('disabled',false);
	$('#clear-english-revise-button').prop('disabled',false);
	checkMode = 1;
}

function showEnglish(){
	rowsSpan = getCheckedRow().find('span.english-word');
	rowsInput = getCheckedRow().find('input.english-word');
	rowsCheck = getCheckedRow().find('.checker').parent();
	for(row of rowsSpan){
		if($(row).hasClass('hidden')){
			$(row).toggleClass('hidden');
		}
	}
	for(row of rowsInput){
		if(!$(row).hasClass('hidden')){
			$(row).toggleClass('hidden');
		}
	}
	
	for(row of rowsCheck){
		if(!$(row).hasClass('hidden')){
			$(row).toggleClass('hidden');
		}
	}
	$('#hidden-vietnamese-revise-button').prop('disabled',false);
	$('#show-vietnamese-revise-button').prop('disabled',false);
	$('#checkall-vietnamese-revise-button').prop('disabled',true);
	$('#checkall-english-revise-button').prop('disabled',true);
	$('#clear-english-revise-button').prop('disabled',true);
	checkMode = 0;
	hiddenAllRowMessage()
}

function hidenVietNamese(){
	rowsSpan = getCheckedRow().find('span.vietnamese-word');
	rowsInput = getCheckedRow().find('input.vietnamese-word');
	rowsCheck = getCheckedRow().find('.checker').parent();
	for(row of rowsSpan){
		if(!$(row).hasClass('hidden')){
			$(row).toggleClass('hidden');
		}
	}
	
	for(row of rowsInput){
		if($(row).hasClass('hidden')){
			$(row).toggleClass('hidden');
		}
	}
	
	for(row of rowsCheck){
		if($(row).hasClass('hidden')){
			$(row).toggleClass('hidden');
		}
	}
	$('#hidden-english-revise-button').prop('disabled',true);
	$('#show-english-revise-button').prop('disabled',true);
	$('#checkall-english-revise-button').prop('disabled',true);
	
	
	$('#checkall-vietnamese-revise-button').prop('disabled',false);
	$('#clear-vietnamese-revise-button').prop('disabled',false);
	checkMode = 2;
}

function showVietNamese(){
	rowsSpan = getCheckedRow().find('span.vietnamese-word');
	rowsInput = getCheckedRow().find('input.vietnamese-word');
	rowsCheck = getCheckedRow().find('.checker').parent();
	for(row of rowsSpan){
		if($(row).hasClass('hidden')){
			$(row).toggleClass('hidden');
		}
	}
	for(row of rowsInput){
		if(!$(row).hasClass('hidden')){
			$(row).toggleClass('hidden');
		}
	}
	for(row of rowsCheck){
		if(!$(row).hasClass('hidden')){
			$(row).toggleClass('hidden');
		}
	}
	$('#hidden-english-revise-button').prop('disabled',false);
	$('#show-english-revise-button').prop('disabled',false);
	$('#checkall-english-revise-button').prop('disabled',true);
	$('#checkall-vietnamese-revise-button').prop('disabled',true);
	$('#clear-vietnamese-revise-button').prop('disabled',true);
	checkMode = 0;
	hiddenAllRowMessage()
}


function gotoWord(word){
	window.open('https://www.google.com/search?q='+word+'&sxsrf=ALeKk03Z6X7XmMsKcJGIc4zfuPcCDTZyZg:1622722582444&source=lnms&tbm=isch&sa=X&ved=2ahUKEwiRnuHYuPvwAhUBBZQKHSCZDhYQ_AUoAXoECAEQAw&biw=1366&bih=657','_blank');
}
(function (exports) {
  'use strict';
  exports.longestCommonSubsequence = (function () {
    /**
     * Find the lengths of longest common sub-sequences
     * of two strings and their substrings.
     *
     * Complexity: O(MN).
     *
     * @private
     * @param {String} first string
     * @param {String} second string
     * @return {Array} two dimensional array with LCS
     * lengths of input strings and their substrings.
     *
     */
    function getLcsLengths(str1, str2) {
      var result = [];
      for (var i = -1; i < str1.length; i = i + 1) {
        result[i] = [];
        for (var j = -1; j < str2.length; j = j + 1) {
          if (i === -1 || j === -1) {
            result[i][j] = 0;
          } else if (str1[i] === str2[j]) {
            result[i][j] = result[i - 1][j - 1] + 1;
          } else {
            result[i][j] = Math.max(result[i - 1][j], result[i][j - 1]);
          }
        }
      }
      return result;
    }
    /**
     * Find longest common sub-sequences of two strings.
     *
     * Complexity: O(M + N).
     *
     * @private
     * @param {String} first string
     * @param {String} second string
     * @return {Array} two dimensional array with LCS
     * lengths of input strings and their substrings
     * returned from 'getLcsLengths' function.
     *
     */
    function getLcs(str1, str2, lcsLengthsMatrix) {
      var execute = function (i, j) {
        if (!lcsLengthsMatrix[i][j]) {
          return '';
        } else if (str1[i] === str2[j]) {
          return execute(i - 1, j - 1)+i+' ';//str1[i];
        } else if (lcsLengthsMatrix[i][j - 1] > lcsLengthsMatrix[i - 1][j]) {
          return execute(i, j - 1);
        } else {
          return execute(i - 1, j);
        }
      };
      return execute(str1.length - 1, str2.length - 1);
    }
    /**
     * Algorithm from dynamic programming. It finds the longest
     * common sub-sequence of two strings. For example for strings 'abcd'
     * and 'axxcda' the longest common sub-sequence is 'acd'.
     *
     * @example
     * var subsequence = require('path-to-algorithms/src/searching/'+
     * 'longest-common-subsequence').longestCommonSubsequence;
     * console.log(subsequence('abcd', 'axxcda'); // 'acd'
     *
     * @public
     * @module searching/longest-common-subsequence
     * @param {String} first input string.
     * @param {String} second input string.
     * @return {Array} Longest common subsequence.
     */
    return function (str1, str2) {
      var lcsLengthsMatrix = getLcsLengths(str1, str2);
      return getLcs(str1, str2, lcsLengthsMatrix);
    };
  })();
})(typeof window === 'undefined' ? module.exports : window);


