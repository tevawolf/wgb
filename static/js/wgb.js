// 外部リンクは別ウインドウで開く
$(function() {
    $('a[href^=http]').attr('target', '_blank');
});



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
function createAnchorWindow(url, thread_no, from_number, to_number) {
    // すでにポップアップが開いていたら、閉じる
    if($(".ui-dialog").length && $(".ui-dialog").css('display') != 'none') {
        $('.ui-dialog').fadeOut('fast');
        return;
    }

    // Ajax実行
    $.get(
        url,
        {'thread_no': thread_no, 'number': to_number}
        )
    .done(function (data) {
        // 実行後処理
        json = JSON.parse(data);
        $('#show_anchor').children().remove();
        $('#show_anchor').append(json.data);

        $("#show_anchor").dialog({
            modal: false,
            title: json.title,
            show: 250,
            hide: 250,
            position: {my: "left top", at: "left top", of: "#anchor_from_" + from_number + '_to_' + to_number},
        });
        $(".ui-dialog-titlebar-close").hide();
        $('.ui-dialog').fadeIn('fast');

        $(document).on('click', function(e) {
            if (!$(e.target).closest('.ui-dialog').length) {
                $('.ui-dialog').fadeOut('fast');
            }
        });
    });
}

// フィルタリング
function filtering_second(member_id) {
    var val = $("#filter_second" + member_id).val();
    var visible;
    if(val == "true") {
        $("#filter_second_div" + member_id).addClass("bg-secondary");
        $("#filter_second_div" + member_id).removeClass("bg-primary");
        $("#filter_second" + member_id).val("false");
    } else {
        $("#filter_second_div" + member_id).addClass("bg-primary");
        $("#filter_second_div" + member_id).removeClass("bg-secondary");
        $("#filter_second" + member_id).val("true");
    }

    var length = $('.filter_second_member').length
    if (length == 1) {
        var visible = $("#filter_second" + member_id).val();
        if (visible == "true") {
                $("[class='card member" + member_id + "']").css('display', 'block');
        } else {
                $("[class='card member" + member_id + "']").css('display', 'none');
        }
    } else {
        $('.filter_second_member').each(function() {
            var visible = $(this).val();
            if (visible == "true") {
                $("[class='card member" + member_id + "']").fadeIn('fast');
            } else {
                $("[class='card member" + member_id + "']").fadeOut('fast');
            }
        });
    }
}

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