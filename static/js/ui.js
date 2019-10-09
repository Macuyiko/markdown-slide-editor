var editor = null;
var currentRequest = null;
var previewFrame = 'preview-frame';
var currentView = 'slide-view list';
var unsavedChanges = false;

function getFrame(name) {
    return window.frames[name];
}

function debounce(fn, duration) {
    var timer;
    return function() {
        clearTimeout(timer);
        timer = setTimeout(fn, duration);
    }
}

function invokeRender() {
    var code = editor.getValue();
    currentRequest = $.ajax(Flask.url_for('render'), {
        data : JSON.stringify({ text: code, view: currentView }),
        contentType : 'application/json',
        type : 'POST',
        beforeSend : function() {
            if (currentRequest != null)
                currentRequest.abort();
        },
        success: function(data) {
            getFrame(previewFrame).document.getElementById('slide-theme').href = 
                Flask.url_for('static', {'filename': 'themes/slide-' + data['slide_theme'] + '.css'}) + 
                '?r=' + Math.random();
            getFrame(previewFrame).document.getElementById('code-theme').href = 
                Flask.url_for('static', {'filename': 'themes/code-' + data['code_theme'] + '.css'}) + 
                '?r=' + Math.random();
            $(getFrame(previewFrame).document.getElementById('markdown')).html(data['html']);
            getFrame(previewFrame).onContentChanged();
        },
        error: function(e){
            if (e.statusText != 'abort')
                console.log(e);
        }
    });
}

function invokeContentsUnsaved(toggle) {
    if (toggle) {
        $('.glow').show();
        unsavedChanges = true;
    } else {
        $('.glow').hide();
        unsavedChanges = false;
    }
}

function invokeOpenFile() {
    var file = document.getElementById("open").files[0];
    document.getElementById("open").value = '';
    if (!file) return;
    $('#filename').val(file.name);
    var reader = new FileReader();
    reader.readAsText(file, "UTF-8");
    reader.onload = function (evt) {
        editor.setValue(evt.target.result, -1);
        invokeContentsUnsaved(false);
        invokeRender();
    }
    reader.onerror = function (evt) {
        console.log(evt);
    }
}

function invokeOpenFileDialog() {
    $('#open').trigger('click');
}

function invokeSaveFile() {
    var code = editor.getValue();
    var filename = $('#filename').val();
    $.ajax(Flask.url_for('save'), {
        data : JSON.stringify({ text: code, filename: filename }),
        contentType : 'application/json',
        type : 'POST',
        success: function(data) {
            $('.glow').hide();
        },
        error: function(e){
            console.log(e);
        }
    });
}

function invokeToggleView() {
    if (currentView.indexOf('slide-view list') > -1)
        currentView = 'slide-view screen';
    else if (currentView.indexOf('slide-view screen') > -1)
        currentView = 'doc-view';
    else
        currentView = 'slide-view list';
    document.getElementById(previewFrame).src = '/preview/' + currentView;
    setTimeout(invokeRender, 500);
    setTimeout(invokeCursorChanged, 1000);
    setTimeout(applyScreenSize, 1000);
}

function openWindowWithPost(url, windowoption, name, params) {
    var form = document.createElement("form");
    form.setAttribute("method", "post");
    form.setAttribute("action", url);
    form.setAttribute("target", name);
    for (var i in params) {
        if (params.hasOwnProperty(i)) {
            var input = document.createElement('input');
            input.type = 'hidden';
            input.name = i;
            input.value = params[i];
            form.appendChild(input);
        }
    }
    document.body.appendChild(form);
    window.open("post.htm", name, windowoption);
    form.submit();
    document.body.removeChild(form);
}

function openPopup(urlPart, viewOverride) {
    var code = editor.getValue();
    var view = currentView;
    if (viewOverride) view = viewOverride;
    var url = Flask.url_for(urlPart, { 'view': view });
    var window = "toolbar=no,location=no,directories=no,status=no,menubar=no," +
        "scrollbars=yes,resizable=yes,width=780,height=400," +
        "top=" + (screen.height-400) + "," + "left=" + (screen.width-840);
    openWindowWithPost(url, window, "Slide Preview Window", { text: code });
}

function invokePrintView() {
    openPopup('print_preview');
}

function invokePresenterView() {
    openPopup('present_preview', 'slide-view screen present');
}

function invokeNewFile(skipRender) {
    editor.setValue('');
    var today = new Date();
    var date = today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate();
    var time = today.getHours() + "-" + today.getMinutes() +"-"+today.getSeconds();
    var dateTime = date+' '+time;
    $('#filename').val(dateTime + '.md');
    invokeContentsUnsaved(false);
    if (!skipRender) invokeRender();
}

function invokeCursorChanged() {
    var code = editor.getValue();
    var cursor = editor.selection.getCursor();
    var index = editor.session.doc.positionToIndex(cursor);
    var re = /^---/gm;
    var substr = code.substr(0, index);
    var count = ((substr || '').match(re) || []).length;
    getFrame(previewFrame).onPaginationChanged(count);
}

function invokeResized() {
    // Handled by the frame itself
    // getFrame(previewFrame).onResized();
    if (editor) editor.resize();
}

$(function() {
    editor = ace.edit("editor");
    editor.session.setMode("ace/mode/markdown");
    editor.setOptions({
        wrap: true,
        indentedSoftWrap: false,
        spellcheck: true
    });

    editor.getSession().on('change', function() {   invokeContentsUnsaved(true);    });
    $('#filename').on('change', function() {        invokeContentsUnsaved(true);    });

    Split(['#editor-pane', '#preview-pane'], {
        onDragEnd: function() {                     invokeResized();                }});
    $(window).on('resize', function(){              invokeResized();                });

    $('#editor').on('keyup',                        debounce(invokeRender, 800)     );
    editor.selection.on('changeCursor', function(){ invokeCursorChanged();          });

    $('#open').on('change', function(){             invokeOpenFile();               });
    
    $('.icon.new').on('click', function(){          invokeNewFile();                });
    $('.icon.open').on('click', function(){         invokeOpenFileDialog();         });
    $('.icon.save').on('click', function(){         invokeSaveFile();               });
    $('.icon.view').on('click', function(){         invokeToggleView();             });
    $('.icon.print').on('click', function(){        invokePrintView();              });   
    $('.icon.present').on('click', function(){      invokePresenterView();          });

    hotkeys('ctrl+l,ctrl+o,ctrl+s,ctrl+v,ctrl+p,f11', function(event, handler) {
        event.preventDefault();
        switch(handler.key){
            case "f11": invokePresenterView(); break;
            case "ctrl+l": invokeNewFile(); break;
            case "ctrl+o": invokeOpenFileDialog(); break;
            case "ctrl+s": invokeSaveFile(); break;
            case "ctrl+v": invokeToggleView(); break;
            case "ctrl+p": invokePrintView(); break;
        }
        return false;
    });
    
    invokeNewFile(true);
    setTimeout(invokeResized, 1000);

});