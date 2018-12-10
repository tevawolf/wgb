// 文字装飾付加（アンカーをリンクにするのもここで）
function add_decorate_tag(tag) {
    if (tag == '%c') {
        var color = $('#colorpicker').val();
        $('#id_sentence').selection('insert', { text: '[' + color + ']' + tag, mode: 'before' });
    } else {
        $('#id_sentence').selection('insert', { text: tag, mode: 'before' });
    }
    $('#id_sentence').selection('insert', { text: tag, mode: 'after' });
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
function filtering(id) {
    // チェックした人だけ表示（複数選択可能）にしたい！！！
    checked_list = $('[class=filter_member]');
    alert(checked_list)

    for(var chk in checked_list) {
        alert(chk.prop('checked'));
    }
    if (checked) {
        $("[class^='card member']").not("[class$='" + id + "']").css('display', 'None');
    } else {
        $("[class^='card member']").not("[class$='" + id + "']").css('display', 'block');
    }
}