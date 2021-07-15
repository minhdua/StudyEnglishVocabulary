var isHidden = false;
$('document').ready(function (){
	createTable();
	$('#btn-hidden').click(function(){
		offOnEnglishList();
	})
	$('#btn-check').click(function(){

		checkEnglishList();
	});
	
	$('#btn-random').click(function(){
		console.log('hello');
		shuffle(vocabularies);
		$('#vocabularies-table tbody').html('');
		createTable();
	});
});

function shuffle(array) {
  var currentIndex = array.length,  randomIndex;

  // While there remain elements to shuffle...
  while (0 !== currentIndex) {

    // Pick a remaining element...
    randomIndex = Math.floor(Math.random() * currentIndex);
    currentIndex--;

    // And swap it with the current element.
    [array[currentIndex], array[randomIndex]] = [
      array[randomIndex], array[currentIndex]];
  }
  return array;
}

function createTable(){
	for(v of vocabularies){
		addRow(v);
	}

	rows = $('.displayRow .displayCell input:checkbox');
	for(row of rows){
		$(row).click(function() {
				mCheckbox = $(this);
				if(mCheckbox.is(':checked')){
					checkboxs = $('.displayCell input:checkbox');
					allchecked = true;
					for(chk of checkboxs){
						if(!$(chk).is(':checked')){
						   allchecked=false;
						}
					}
					if(allchecked){
						$('.headerCell input:checkbox').prop('checked',true);
					}
				}else{
					$('.headerCell input:checkbox').prop('checked',false);
				}
		});
	}
	
	$('.headerCell input:checkbox').click(function(){
		if($(this).is(':checked')){
			$('.displayRow input:checkbox').prop('checked',true);
		}else{
			$('.displayRow input:checkbox').prop('checked',false);
		}
	});	
}
document.onkeyup = function (e) {
    var evt = window.event || e;   
    if ((evt.keyCode == 38 || evt.keyCode == 40)&& evt.altKey) {
        $('#btn-hidden').click();   
    }1
	if ((evt.keyCode == 13) && evt.altKey) {
        $('#btn-check').click();   
    }
}

function maxRow(){
	return $('.displayRow').length;
}

function addRow(v){
	maxR = maxRow();
	$('#vocabularies-table').append('<tr id ="'+maxRow()+'" class="displayRow"> <td class="cell displayCell"> <input type="checkbox"/> </td> <td class="cell displayCell"> <span class="noValue"> '+(maxRow()+1)+' </span> <span class="noValue hidden">'+v.no+'</span> </td> <td class="cell displayCell"> <span class="englishValue"> '+v.english+' </span> <input onkeypress="focusBlankCell.call(this,event)" class="englishValue hidden"\>	</td> <td class="cell displayCell"> <span class="vietnameseValue"> '+v.vietnamese+' </span> </td> </tr>');
}

function getCheckedList(){
	return $('.displayCell input:checked').parents('tr');
}

function hidden(selector){
	if(!selector.hasClass('hidden')){
		selector.toggleClass('hidden');
	}
}

function show(selector){
	if(selector.hasClass('hidden')){
		selector.toggleClass('hidden');
	}
}

function hiddenEnglish(row){
	show($(row).find('input.englishValue'));
	hidden($(row).find('span.englishValue'));
}

function showEnglish(row){
	$(row).find('input.englishValue').val('');
	hidden($(row).find('input.englishValue'));
	show($(row).find('span.englishValue'));
}

function checkEnglish(row){
	value = $(row).find('input.englishValue').val().trim();
	text =  $(row).find('span.englishValue').text().trim();
	if(value === undefined || text === undefined) return false;
	return value.toLowerCase() === text.toLowerCase();
}

function offOnEnglishList(){
	rows = getCheckedList();
	if(isHidden){
		isHidden = false;
		for(row of rows){
			showEnglish(row);
		}
	}else{
		isHidden = true;
		for(row of rows){
			hiddenEnglish(row);
		}
	}
}

function markError(row){
	selector = $(row).find('span.englishValue').parents('td');
	if(!selector.hasClass('error')){
		selector.toggleClass('error');
	}
}

function unmarkError(row){
	selector = $(row).find('span.englishValue').parents('td');
	if(selector.hasClass('error')){
		selector.toggleClass('error');
	}
}

function uncheckedRow(row){
	$(row).find('input:checkbox').click();
}

function convertListToText(list){
	txt = "";
	for(e of list){
		txt += e + ",";
	}
	return txt;
}

function checkEnglishList(){
	rows = getCheckedList();
	orderErrorList = [];
	$('.compare').html('');
	$('#error-detail').html('');
	for(row of rows){
		if(checkEnglish(row)){
			showEnglish(row);
			unmarkError(row);
			uncheckedRow(row);
		}else{
			markError(row);
			order = $(row).find('.noValue.hidden').text();
			orderErrorList.push(order);
		}
	}
	if(0 === orderErrorList.length){
		if(!$('#error-detail').hasClass('hidden')){
			$('#error-detail').toggleClass('hidden');
		}
	}else{
		if($('#error-detail').hasClass('hidden')){
			$('#error-detail').toggleClass('hidden');
		}
		message = convertListToText(orderErrorList);
		$('#error-detail').html(message);
	}
	$('.compare').html(getCompareList());
}

function focusBlankCell(e){
	e = e || window.event;
	if((e.keyCode ? e.keyCode : e.which) == 13){
        row = $(this).parents('.displayRow').get(0);
		nextRow = findNextBlankCell(row);
		$(nextRow).find('input:text').focus();
    }
	if(this.value.length >30){
		this.style.width = ((this.value.length + 1) * 8) + 'px';
	}else{
		this.style.width = 30 + 'px';
	}
}

function findNextBlankCell(rowCurrent){
	rows = getCheckedList();
	var rowRetention = rowCurrent;
	for(row of rows){
		value = $(row).find('input:text').val();
		if(row === rowCurrent) break;
		rowRetention = row;
	}
	return rowRetention;
}

function getCompareList(){
	list = getCheckedList();
	var textList = "";
	for(e of list){
		englishSpan = $(e).find('.englishValue').text();
		englishInput = $(e).find('input.englishValue').val();
		if(englishInput.length>0){
			listSpan = englishSpan.trim().split(" ");
			listInput = englishInput.split(" ");
			n = listSpan.length;
			if(listInput.length < listSpan.length){
				n = listInput.length;
			}
			textList +="<p>";
			for(i = 0 ;i < n; i++){
				if(listSpan[i].toLowerCase() != listInput[i].toLowerCase()){
					textList += " "+listInput[i]+" ["+listSpan[i]+"] ";
				}else{
					textList += " "+ listInput[i]+" ";
				}
			}
			textList += "<\p>";
		}
		
	}
	return textList;
}
