window.focused_input = false;
window.drag_just_happened = false;  // Because mouseout happens after drag.
function message_init() {
  $('#message span').each(function(i, elt) {
    $(elt).click(function(evt) {
      if(drag_just_happened) {
        drag_just_happened = false;
        return;
      }
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
}
$(function() {
  $('.form-field input, .form-field textarea').each(function(i, elt) {
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
        var sep = cur_val.length > 0 ? ' ' : '';
        $(evt.srcElement).addClass('used');
        $(this).val(cur_val + sep + word);
        $(evt.srcElement).css({ 'top': '0px', 'left': '0px' });
      },
      over: function(evt, ui) {
        $(this).addClass('selected');
        drag_just_happened = true;
      },
      out: function(evt, ui) {
        $(this).removeClass('selected');
      },
      deactivate: function(evt, ui) {
        $(evt.srcElement).css({ 'top': '0px', 'left': '0px' });
        $(this).removeClass('selected');
      }
    });
  });
  message_init();
});
