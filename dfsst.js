function txtls2html(ls) {
  return ls.map(function(blob) {
    return '<span class="'+blob.lang+'">'+blob.txt+'</span>';
  }).join('');
}

function sentence_button() {
  $(this).toggle();
  $(this).parent().find('p').toggle();
}

function display_day(idx) {
  let blob = DAYS[idx];
  $('#vocab').html(blob.vocab.map(function(voc) {
    return '<li><span class="st headword">'+voc.word+'</span>&nbsp;'+txtls2html(voc.def)+'</li>';
  }).join(''));
  $('#comments').html(blob.comments.map(function(com) {
    return '<p class="comment">'+txtls2html(com)+'</p>';
  }).join(''));
  let sents = blob.sentences.slice(0);
  let st_ct = sents.length / 2;
  let sent_html = '';
  while (sents.length > 0) {
    let sb = sents.splice(Math.floor(Math.random() * sents.length), 1)[0];
    if (sents.length >= st_ct) {
      sent_html += '<div class="sentence"><p class="st">'+sb.st+'</p><div class="answer"><button class="sentbut">Show English</button><p class="en">'+sb.en+'</p></div>';
    } else {
      sent_html += '<div class="sentence"><p class="en">'+sb.en+'</p><div class="answer"><button class="sentbut">Show Sajem Tan</button><p class="st">'+sb.st+'</p></div>';
    }
  }
  $('#sentences').html(sent_html);
  $('.sentbut').click(sentence_button);
  $('.answer p').hide();
  if (blob.hasOwnProperty('reading')) {
    $('#reading').html('<h2>Reading</h2><p>'+blob.reading+'</p>');
  } else {
    $('#reading').html('');
  }
  if (idx == 0) {
    $('#prev').hide();
  } else {
    $('#prev').show().click(function() { display_day(idx-1); });
  }
  if (idx+1 == DAYS.length) {
    $('#next').hide();
  } else {
    $('#next').show().click(function() { display_day(idx+1); });
  }
  $('#intro').hide();
  $('#day').show();
}

$(document).ready(function() {
  $('#day').hide();
  $('#exit').click(function() {
    $('#day').hide();
    $('#intro').show();
  });
  $('#nonexistent').hide();
  $('#go').click(function() {
    $('#nonexistent').hide();
    let idx = parseInt($('#cycle').val()) * 30 + parseInt($('#letter').val());
    if (idx < DAYS.length) {
      display_day(idx);
    } else {
      $('#nonexistent').show();
    }
  });
});
