$(document).ready(function() {
    function delayedAction(sender, action, interval) {
        if(!interval) {
            interval = 500;
        }
        if(sender.promise_) {
            clearTimeout(sender.promise_);
        }
        sender.promise_ = setTimeout(action, interval);
    }

    var EXAMPLE_TEXT;
    var ANIMATION_ON = false;
    function searchExample() {
        setTimeout(function() {
            $('#SearchInput').autocomplete('close');
            $('#SearchBtn').toggleClass('active');
            $('#SearchBtn').click();
            ANIMATION_ON = false;
        }, 600);
    }
    window.selectExample = function() {
        if ($('#ui-id-1').css('display') == 'none') {
            $('#SearchInput').val(EXAMPLE_TEXT);
            searchExample();
            return;
        }
        var e = jQuery.Event("keydown");
        e.keyCode = 40;
        $('#SearchInput').trigger(e);
        if ($('#SearchInput').val() == EXAMPLE_TEXT) {
            searchExample();
            return;
        }
        window.setTimeout("selectExample()", 150);
    }

    var CACHE = {};
    var RESPONSE_READY = true;
    function setupAutoComplete(url, inputId, resultId) {
        $(inputId).autocomplete({
            appendTo: resultId,
            delay: 500,
            minLength: 1,
            source: function(request, response) {
                var q = request.term;
                // TODO
                var qkey = String($('#CorpusSelector').val()) + ': ' + q;
                if (qkey in CACHE) {
                    response(CACHE[qkey]);
                    return;
                }
                $.ajax({
                    url: url,
                    dataType: 'json',
                    data:{q: q, c: $('#CorpusSelector').val()},
                    success: function(r) {
                        var data = $.map(r.gr, function(item){
                            // TODO using template to render
                            var s = item[1];
                            var p1 = s.indexOf('<strong>'), p2 = s.lastIndexOf('</strong>');
                            var begin = Math.max(p1 - Math.floor((74-(p2-p1-25))/2), 0);
                            if(begin > 0 && s[begin] != ' ' && s[begin-1] != ' '){
                                begin += s.slice(begin).indexOf(' ') + 1;
                            }
                            s = s.slice(begin);
                            if(begin > 0)
                                s = '...' + s;
                            var label = '<p class="suggestWord textOverflow">'+ item[0] + '</p>' + '<p class="exampleSentence textOverflow">' + s + '</p>';
                            return {value: item[0], label: label};
                        });
                        CACHE[qkey] = data;
                        response(data);
                    },
                    fail: function() {
                        response([]);
                    }
                });
            },
            open: function (event, ui) {
                if (RESPONSE_READY == false) {
                    RESPONSE_READY = true;
                    window.setTimeout("selectExample()", 200);
                }
            },
            html: true
        });
    }
    if($('#SearchInput').length>0){
        setupAutoComplete(DEP_URL, '#SearchInput', '#SuggestionContainer');
        $('#SearchInput').focus();
    }
    else if($('#NavSearchInput').length>0){
        setupAutoComplete(DEP_URL, '#NavSearchInput', '#SuggestionContainer');
        $('#NavSearchInput').focus();
    }

    function scrollToTop(duration, callback) {
        var x = 0, initialY = scrollY, ease = function(n) {
            return n * (2 - n);
        };
        const interval = setInterval(function () {
            x += 20 / duration;
            scrollTo(scrollX, x > 1 ? 0 : (1 - ease(x)) * initialY);
            if (x > 1) {
                clearInterval(interval);
                callback && callback();
            }
        }, 20);
    }

    function fillWithExample(text) {
        // scroll to top
        // clear and fill in text
        // (wait drop down and select suggestion)
        // click search button
        if (ANIMATION_ON || !text) {
            return;
        }
        ANIMATION_ON = true;
        var showAutocomplete = (text.indexOf('*') >= 0 || text.indexOf('(') >= 0);
        var q = text.replace(/\*/g, '').replace(/\(.*?\)/g, '').trim();
        // $('html,body').animate({ scrollTop: 0 }, 'fast', 'swing', function() {
        // for campatibility with Chrome:
        scrollToTop(300, function () {
            $('#SearchInput').val('');
            (function addChar() {
                if (q) {
                    $('#SearchInput').val($('#SearchInput').val() + q[0]);
                    q = q.slice(1);
                    setTimeout(addChar, 80);
                } else {
                    $('#SearchInput').focus();
                    if (showAutocomplete) {
                        RESPONSE_READY = false;
                        EXAMPLE_TEXT = text;
                        $('#SearchInput').autocomplete('search');
                    } else {
                        searchExample();
                    }
                }
            })();
        });
    }

    $('.example-btn-link').click(function() {
        fillWithExample($(this).text());
    });

    // Fix Safari cache on back
    if (navigator.userAgent.indexOf("Safari") >= 0) {
        $(window).bind("pageshow", function (event) {
            if (event.originalEvent.persisted) {
                $("#SearchInput").attr('autocomplete', 'off');
                $("#NavSearchInput").attr('NavSearchInput', 'off');
            }
        });
    }
});


/*
 * jQuery UI Autocomplete HTML Extension
 *
 * Copyright 2010, Scott González (http://scottgonzalez.com)
 * Dual licensed under the MIT or GPL Version 2 licenses.
 *
 * http://github.com/scottgonzalez/jquery-ui-extensions
 */
(function( $ ) {

var proto = $.ui.autocomplete.prototype,
    initSource = proto._initSource;

function filter( array, term ) {
    var matcher = new RegExp( $.ui.autocomplete.escapeRegex(term), "i" );
    return $.grep( array, function(value) {
        return matcher.test( $( "<div>" ).html( value.label || value.value || value ).text() );
    });
}

$.extend( proto, {
    _initSource: function() {
        if ( this.options.html && $.isArray(this.options.source) ) {
            this.source = function( request, response ) {
                response( filter( this.options.source, request.term ) );
            };
        } else {
            initSource.call( this );
        }
    },

    _renderItem: function( ul, item) {
        return $( "<li></li>" )
            .data( "item.autocomplete", item )
            .append( $( "<a></a>" )[ this.options.html ? "html" : "text" ]( item.label ) )
            .appendTo( ul );
    }
});

})( jQuery );
