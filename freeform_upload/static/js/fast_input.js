$(function() {
  var focused_input = false;
  $('.form-field input').each(function(i, elt) {
    $(elt).bind('focus', _.bind(function() {
      if(focused_input) {
        $(focused_input).removeClass('selected');
      }
      focused_input = this;
      $(this).addClass('selected');
    }, elt));
    $(elt).droppable({
      drop: function(evt, ui) {
        var word = $(evt.srcElement).text();
        var cur_val = $(this).val();
        if(cur_val === undefined) {  // No focused input
          return;
        }
        var sep = cur_val.length > 0 ? ' ' : '';
        $(evt.srcElement).addClass('used');
        $(this).val(cur_val + sep + word);
        $(evt.srcElement).css({ 'top': '0px', 'left': '0px' });
      },
      over: function(evt, ui) {
        $(this).addClass('selected');
      },
      out: function(evt, ui) {
        $(this).removeClass('selected');
      },
      deactivate: function(evt, ui) {
        $(evt.srcElement).css({ 'top': '0px', 'left': '0px' });
      }
    });
  });
  $('#message span').each(function(i, elt) {
    $(elt).click(function(evt) {
      var word = $(evt.currentTarget).text();
      var cur_val = $(focused_input).val();
      if(cur_val === undefined) {  // No focused input
        return;
      }
      var sep = cur_val.length > 0 ? ' ' : '';
      $(evt.currentTarget).addClass('used');
      $(focused_input).val(cur_val + sep + word);
    });
    $(elt).draggable();
  });
});
