// 文字装飾付加（アンカーをリンクにするのもここで）
function add_decorate_tag(tag, selector) {
    if (tag == '%c') {
        var color = $('#colorpicker').val();
        $('#id_' + selector).selection('insert', { text: '[' + color + ']' + tag, mode: 'before' });
    } else {
        $('#id_' + selector).selection('insert', { text: tag, mode: 'before' });
    }
    $('#id_' + selector).selection('insert', { text: tag, mode: 'after' });
}

// アンカークリック　ウインドウ表示
function createAnchorWindow(url, thread_no, number) {
    // Ajax実行
    $.get(
        url,
        {'thread_no': thread_no, 'number': number}
        )
    .done(function (data) {
        // 実行後処理
        json = JSON.parse(data);
        $('#show_anchor').children().remove();
        $('#show_anchor').append(json.data);

        $("#show_anchor").dialog({
            modal: false,
            title: "アンカーポップアップ",
            show: 250,
            hide: 250,
        });
    });
}

// フィルタリング
function filtering() {
    // チェックした人だけ表示（複数選択可能）にしたい！！！
    $('[class=filter_member]:checked').each(function() {
        var member_id = $(this).val();
        $("[class='card member" + member_id + "']").fadeIn(200);
    });
    $(':not([class=filter_member]:checked)').each(function() {
        var member_id = $(this).val();
        $("[class='card member" + member_id + "']").fadeOut(200);
    });
}