$(document).ready(function() {
    $('.article .read-form').hide().ajaxForm();
    $('.article').click(function() {
        $('.article').removeClass('selected');
        var article = $(this);
        article.addClass('selected');
        article.find('.read-form').ajaxSubmit();
    });
});
