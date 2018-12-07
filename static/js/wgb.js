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
    /* https://syncer.jp/jquery-modal-window */
    function createAnchorWindow(url, thread_no, number) {
        //キーボード操作などにより、オーバーレイが多重起動するのを防止する
        $(this).blur() ;	//ボタンからフォーカスを外す
        if($("#modal-overlay")[0]) return false ;		//新しくモーダルウィンドウを起動しない [下とどちらか選択]
        //if($("#modal-overlay")[0]) $("#modal-overlay").remove() ;		//現在のモーダルウィンドウを削除して新しく起動する [上とどちらか選択]

        //オーバーレイ用のHTMLコードを、[body]内の最後に生成する
        $("body").append('<div id="modal-overlay"></div>');

        //[$modal-overlay]をフェードインさせる
        $("#modal-overlay").fadeIn("fast");

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

            centeringModalSyncer();

            $("#show_anchor").fadeIn("fast");

            $("#modal-overlay, #modal-close").unbind().click( function() {
                $("#show_anchor, #modal-overlay").fadeOut("fast", function() {
                    //フェードアウト後、[#modal-overlay]をHTML(DOM)上から削除
                    $("#modal-overlay").remove();
                });
            });
        });

        centeringModalSyncer();
    }

    //センタリングをする関数
    function centeringModalSyncer() {

        var w = $(window).width();
        var h = $(window).height();

        //コンテンツ(#modal-content)の幅を取得し、変数[cw]に格納
        var cw = $("#modal-content").outerWidth();
        //コンテンツ(#modal-content)の高さを取得し、変数[ch]に格納
        var ch = $("#modal-content").outerHeight();

        //コンテンツ(#modal-content)を真ん中に配置するのに、左端から何ピクセル離せばいいか？を計算して、変数[pxleft]に格納
        var pxleft = ((w - cw) / 2);
        //コンテンツ(#modal-content)を真ん中に配置するのに、上部から何ピクセル離せばいいか？を計算して、変数[pxtop]に格納
        var pxtop = ((h - ch) / 2);

        //[#modal-content]のCSSに[left]の値(pxleft)を設定
        $("#modal-content").css({"left": pxleft + "px"});
        //[#modal-content]のCSSに[top]の値(pxtop)を設定
        $("#modal-content").css({"top": pxtop + "px"});
    }

$(function(){

//リサイズされたら、センタリングをする関数[centeringModalSyncer()]を実行する
$( window ).resize( centeringModalSyncer ) ;

} ) ;