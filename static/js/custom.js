$(document).ready(function() {
    var is_update = false;
    var can_update_slide = true;
    //$("#keranjang-diterima").load(BASE_URL + 'product/show_cart/', init_slider);
    var current_pathname = window.location.pathname;
    if(current_pathname.search(/receive/i) > 0) {
        load_table_keranjang_penerimaan();
    } else if(current_pathname.search(/return/i) > 0) {
        load_table_keranjang_pengembalian();
    }
    $('#daftar-merk').dataTable({
        "processing": true,
        "serverSide": true,
        "ajax": BASE_URL + "merk/data/",
        columnDefs: [
             { orderable: false, targets: [-1, -2] }
        ]
    });
    $('#daftar-produk').dataTable({
        "processing": true,
        "serverSide": true,
        "ajax": BASE_URL + "product/data/",
        columnDefs: [
             { orderable: false, targets: [-1] }
        ]
    });
    $('#daftar-gudang').dataTable({
        "processing": true,
        "serverSide": true,
        "ajax": BASE_URL + "warehouse/data/",
        columnDefs: [
             { orderable: false, targets: [-1,-2] }
        ]
    });
    $('#daftar-pelanggan').dataTable({
        "processing": true,
        "serverSide": true,
        "ajax": BASE_URL + "customer/data/",
        columnDefs: [
             { orderable: false, targets: [-1] }
        ]
    });
    $('#daftar-diskon').dataTable({
        "processing": true,
        "serverSide": true,
        "ajax": BASE_URL + "discount/data/",
        columnDefs: [
             { orderable: false, targets: [-1] }
        ]
    });
    $('#daftar-stok').dataTable({
        "processing": true,
        "serverSide": true,
        "ajax": BASE_URL + "stock/data/",
        columnDefs: [
             { orderable: false, targets: [-1] }
        ]
    });
    $('#daftar-pengguna').dataTable({
        "processing": true,
        "serverSide": true,
        "ajax": BASE_URL + "accounts/data/",
        columnDefs: [
             { orderable: false, targets: [-1] }
        ]
    });
    $('#daftar-produk-gudang').dataTable({
        "processing": true,
        "serverSide": true,
        "ajax": BASE_URL + $('#daftar-produk-gudang').data('url'),
        columnDefs: [
             { orderable: false, targets: [-1] }
        ]
    });

    $(".js-example-matcher-start").select2({
        ajax: {
            url: BASE_URL + 'product/list_json',
            dataType: 'json'
        },
        matcher: matchStart
    });
    $(".js-example-matcher-start").change(function() {
        if($(this).val()) {
            //$('#btn-mapping-gudang').removeClass('disabled');
            $.ajax({
                url: BASE_URL + 'product/receive/add/' + $(this).val(),
                cache: false,
                success: function(html){
                    /*$.get(BASE_URL + 'product/show_cart/', function(html) {
                        $("#keranjang-diterima").html(html);
                    });*/
                    //$("#keranjang-diterima").load(BASE_URL + 'product/show_cart/', init_slider);
                    //$("#total-harga-diterima").load(BASE_URL + 'product/cart_total/');
                    load_table_keranjang_penerimaan();
                    $(".js-example-matcher-start").val(null).trigger("change"); 
                    //$('.txt-qty').editable();
                }
            });

        } else {
            //$('#btn-mapping-gudang').addClass('disabled');
        }
    });
    $('#btn-mapping-gudang').click(function() {
        if(!$(this).hasClass('disabled')) {
            $('#row-mapping-gudang').removeClass('hidden');
            if($.fn.DataTable.isDataTable('#mapping-gudang')) {
                $('#mapping-gudang').dataTable().fnDestroy();
            }
            $('#mapping-gudang').dataTable({
                "processing": true,
                "serverSide": true,
                "ajax": BASE_URL + 'product/mapping/' + $(".js-example-matcher-start").val() + '/'
            });
        }
    });

    $('#btn-tambah-produk').click(function() {
        $.ajax({
            url: BASE_URL + 'product/modal_create/',
            cache: false,
            success: function(html){
                $("#body-tambah-produk").html(html);
                $('#modal-tambah-produk').modal('show');
            }
        });
    });
    $('#mapping-gudang').on('click', 'button[id^=show-mapping-]', function() {
        var elem_tr = $("#tr-mapping-" + $(this).attr('id').substr(13));
        if(elem_tr.is(':visible')) {
            $("#mapping-" + $(this).attr('id').substr(13)).slideToggle("slow");
            $("#show-mapping-" + $(this).attr('id').substr(13)).html('<i class="fa fa-chevron-up"></i> Gudang');
            elem_tr.hide();
        } else {
            elem_tr.show();
            $("#mapping-" + $(this).attr('id').substr(13)).slideToggle("slow");
            $("#show-mapping-" + $(this).attr('id').substr(13)).html('<i class="fa fa-chevron-down"></i> Gudang');
        }
        event.preventDefault();
    });

    $('#mapping-gudang').on('keyup keypress blur change', 'input[class*="stock-slider2-"]', function(event) {
        if(can_update_slide) {
            var pk = $(this).data('pk');
            var sisa = parseInt($('.sisa-' + pk).text());
            var prev = parseInt($(this).data('prev'));
            var patt = /stock-slider2-([0-9+])-([0-9+])/i;
            var a = $(this).attr('class').match(patt);
            if((sisa - ($(this).val() - prev) >= 0) && ($(this).val() != prev)) {
                $('.sisa-' + $(this).data('pk')).text(sisa - ($(this).val() - prev));
                $('#txt-sisa-' + pk).val(sisa - ($(this).val() - prev));
                $(this).val($(this).val());
                $(this).data('prev', $(this).val());
                $('.stock-input-' + pk + '-' + a[2]).val($(this).val());
                is_update = true;
                can_update_slide = false;
                $('input[class*="stock-slider2-' + pk + '-"]').each(function(i, el){
                    update_slider($(el), parseInt($(el).data('prev'))+parseInt($('.sisa-' + pk).text()));
                });
                //update_slider(el, prev+sisa);
            } else {
                $(this).val(prev);
                $('.stock-input-' + pk + '-' + a[2]).val(prev);
                is_update = true;
                can_update_slide = false;
                update_slider($(this), prev);
            }
        }
    });

    $('#mapping-gudang').on('change keyup', 'input[class*="stock-input-"]', function(event) {
        var patt = /stock-input-([0-9+])-([0-9+])/i;
        var a = $(this).attr('class').match(patt);
        var $elem = $('.stock-slider2-' + a[1] + '-' + a[2]);
        var pk = $elem.data('pk');
        var sisa = parseInt($('.sisa-' + pk).text());
        var prev = parseInt($elem.data('prev'));
        var slider = $elem.data("ionRangeSlider");
        if((sisa - ($(this).val() - prev) >= 0) && ($(this).val != prev)) {
            slider.update({
                from: $(this).val()
            });
        } else {
            $(this).val(prev);
        }
    });

    function update_slider(elem, max) {
        if(is_update) {
            var slider = elem.data("ionRangeSlider");
            slider.update({
                max: max
            });
            is_update = false;
            can_update_slide = true;
        }
    }

    $('#mapping-gudang').editable({
        selector: '.txt-qty',
        success: function(response, newValue) {
            /*$('#txt-subtotal-' + response.pk).text(response.price);
            $('.sisa-' + response.pk).text(response.qty);
            var sum = 0;

            $('#keranjang-diterima input[class*="stock-slider2-' + response.pk + '-"]').each(function(i, el){
                var patt = /stock-slider2-([0-9+])-/i;

                
                var spl = el.className.split(' ');
                for(var i=0;i < spl.length; i++) {
                    if(spl[i].match(patt)) {
                        sum = sum + parseInt($('.' + spl[i]).data('prev'));
                    }
                }
            });
            $('.sisa-' + response.pk).text(response.qty - sum);*/
            //$("#keranjang-diterima").load(BASE_URL + 'product/show_cart/', init_slider);
            //$("#total-harga-diterima").load(BASE_URL + 'product/cart_total/');
            load_table_keranjang_penerimaan();
        }
    });

    $('#mapping-gudang').on('click', '.tambah-gudang-penerimaan', function() {
        $('#select-tambah-gudang').html('');
        $('#modal-tambah-gudang').modal('show');
        $('#text-tambah-gudang').text('Menambah Gudang untuk Produk ' + $(this).data('namaproduk'));
        var produk_id = $(this).data('produk');
        $('#form-tambah-gudang').append('<select class="form-control" id="select-tambah-gudang" name="warehouse[' + produk_id + ']"></select>');
        $.ajax({
            url: BASE_URL + 'warehouse/list_warehouse/' + produk_id + '/',
            cache: false,
            success: function(res){
                $('#hidden-product-id').val(produk_id);
                $.each(res.results, function(key, value) {
                    $('#select-tambah-gudang')
                        .append($("<option></option>")
                            .attr("value", value.id)
                            .text(value.text)); 
                });

            }
        });
    });

    $('#save-tambah-gudang').click(function() {
        swal({
            title: 'Konfirmasi',
            text: "Apa anda yakin akan menambah gudang untuk produk ini?",
            type: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Ok',
            cancelButtonText: 'Cancel'
        }).then(function () {
            $('#hidden-warehouse-id').val($('#select-tambah-gudang').val());
            var produk_id = $('#hidden-product-id').val();
            var warhouse_id = $('#hidden-warehouse-id').val();
            var data = $("form#form-keranjang-penerimaan").serialize() + '&' + $("form#form-tambah-gudang").serialize() + '&range[' + produk_id + '][' + warhouse_id + ']=0';
            $.ajax({
                type: "POST",
                url: BASE_URL + 'product/receive/testpost/',
                data: data,
                cache: false,
                success: function(res){
                    $.ajax({
                        url: BASE_URL + 'product/receive/show_cart/',
                        cache: false,
                        success: function(res){
                            $("#mapping-gudang").html($(res));
                            init_slider();
                            $('#hidden-product-id').val('');
                            $('#hidden-warehouse-id').val('');
                            $('#modal-tambah-gudang').modal('hide');
                        }
                    });
                    $("#total-harga-diterima").load(BASE_URL + 'product/receive/cart_total/');
                }
            });
        });
    });

    $('.submit-keranjang-penerimaan').click(function() {
        var punya_sisa = false;
        var elem = '';
        var sum = 0;
        $('#mapping-gudang span[class*="sisa"]').each(function(i, el){
            elem = $(el);
            sum = sum + parseInt(elem.text());
        });
        if(parseInt(elem.text()) > 0) {
            swal(
              'Oops...',
              'Masih ada produk yang mempunyai sisa stok',
              'error'
            );
        } else {
            swal({
                title: 'Konfirmasi',
                text: "Apa anda yakin akan menerima semua barang ini?",
                type: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: 'Ok',
                cancelButtonText: 'Cancel'
            }).then(function () {
                var data = $("form#form-keranjang-penerimaan").serialize() + '&' + $("form#form-tambah-gudang").serialize() + '&range[1][' + $('#select-tambah-gudang').val() + ']=0';
                $.ajax({
                    type: "POST",
                    url: BASE_URL + 'product/receive/checkout/',
                    data: data,
                    cache: false,
                    success: function(res){
                        swal(
                          'Success',
                          'Berhasil menerima produk!',
                          'success'
                        )
                        $.ajax({
                            url: BASE_URL + 'product/receive/show_cart/',
                            cache: false,
                            success: function(res){
                                $("#mapping-gudang").html($(res));
                                init_slider();
                            }
                        });
                        $("#total-harga-diterima").load(BASE_URL + 'product/receive/cart_total/');
                    }
                });
            });
        }
    });

    (function() {
        var original = $.fn.editableutils.setCursorPosition;
        $.fn.editableutils.setCursorPosition = function() {
            try {
                original.apply(this, Array.prototype.slice.call(arguments));
            } catch (e) { /* noop */ }
        };
    })();

    /* Pengembalian Produk */
    $(".js-matcher-returned").select2({
        ajax: {
            url: BASE_URL + 'product/list_json',
            dataType: 'json'
        },
        matcher: matchStart
    });
    $(".js-matcher-returned").change(function() {
        if($(this).val()) {
            $.ajax({
                url: BASE_URL + 'product/return/add/' + $(this).val(),
                cache: false,
                success: function(html){
                    load_table_keranjang_pengembalian();
                    $(".js-matcher-returned").val(null).trigger("change"); 
                }
            });

        }
    });
    $('.submit-keranjang-pengembalian').click(function() {
        var punya_sisa = false;
        var elem = '';
        var sum = 0;
        $('#mapping-gudang span[class*="sisa"]').each(function(i, el){
            elem = $(el);
            sum = sum + parseInt(elem.text());
        });
        if(parseInt(elem.text()) > 0) {
            swal(
              'Oops...',
              'Masih ada produk yang mempunyai sisa stok',
              'error'
            );
        } else {
            swal({
                title: 'Konfirmasi',
                text: "Apa anda yakin akan mengembalikan semua barang ini?",
                type: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: 'Ok',
                cancelButtonText: 'Cancel'
            }).then(function () {
                var data = $("form#form-keranjang-pengembalian").serialize();
                $.ajax({
                    type: "POST",
                    url: BASE_URL + 'product/return/checkout/',
                    data: data,
                    cache: false,
                    success: function(res){
                        swal(
                          'Success',
                          'Berhasil mengembalikan produk!',
                          'success'
                        )
                        $.ajax({
                            url: BASE_URL + 'product/return/show_cart/',
                            cache: false,
                            success: function(res){
                                $("#mapping-gudang").html($(res));
                                init_slider();
                            }
                        });
                        $("#total-harga-diterima").load(BASE_URL + 'product/return/cart_total/');
                    }
                });
            });
        }
    });
});
function init_slider() { 
    $('#mapping-gudang input[class*="stock-slider2-"]').each(function(i, el){
        var prev = parseInt($(this).data('prev'));
        var patt = /stock-slider2-([0-9+])-/i;
        var a = $(this).attr('class').match(patt);
        var pk = a[1]
        var sisa = parseInt($('.sisa-' + pk).text());

        $('.' + el.className).ionRangeSlider({
            min:0,
            max: prev+sisa
        });
    });
}
function load_table_keranjang_penerimaan() {
    $.ajax({
        type: "POST",
        url: BASE_URL + 'product/receive/testpost/',
        data: $("form#form-keranjang-penerimaan").serialize(),
        cache: false,
        success: function(res){
            $.ajax({
                url: BASE_URL + 'product/receive/show_cart/',
                cache: false,
                success: function(res){
                    $("#mapping-gudang").html($(res));
                    init_slider();
                }
            });
            //$("#keranjang-diterima").load(BASE_URL + 'product/show_cart/', init_slider);
            $("#total-harga-diterima").load(BASE_URL + 'product/receive/cart_total/');
            //init_slider();
        }
    });
    //("#keranjang-diterima").load(BASE_URL + 'product/show_cart/', init_slider);
}
function load_table_keranjang_pengembalian() {
    $.ajax({
        type: "POST",
        url: BASE_URL + 'product/return/testpost/',
        data: $("form#form-keranjang-pengembalian").serialize(),
        cache: false,
        success: function(res){
            $.ajax({
                url: BASE_URL + 'product/return/show_cart/',
                cache: false,
                success: function(res){
                    $("#mapping-gudang").html($(res));
                    init_slider();
                }
            });
            $("#total-harga-dikembalikan").load(BASE_URL + 'product/return/cart_total/');
        }
    });
}
function hapus_merk(id) {
    swal({
        title: 'Konfirmasi',
        text: "Apa anda yakin ingin menghapus merk ini?",
        type: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Ok',
        cancelButtonText: 'Cancel'
    }).then(function () {
        window.location.href = BASE_URL + 'merk/delete/' + id;
    })
}
function hapus_produk(id) {
    swal({
        title: 'Konfirmasi',
        text: "Apa anda yakin ingin menghapus produk ini?",
        type: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Ok',
        cancelButtonText: 'Cancel'
    }).then(function () {
        window.location.href = BASE_URL + 'product/delete/' + id;
    })
}
function hapus_gudang(id) {
    swal({
        title: 'Konfirmasi',
        text: "Apa anda yakin ingin menghapus gudang ini?",
        type: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Ok',
        cancelButtonText: 'Cancel'
    }).then(function () {
        window.location.href = BASE_URL + 'warehouse/delete/' + id;
    })
}
function hapus_pelanggan(id) {
    swal({
        title: 'Konfirmasi',
        text: "Apa anda yakin ingin menghapus pelanggan ini?",
        type: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Ok',
        cancelButtonText: 'Cancel'
    }).then(function () {
        window.location.href = BASE_URL + 'customer/delete/' + id;
    })
}
function hapus_diskon(id) {
    swal({
        title: 'Konfirmasi',
        text: "Apa anda yakin ingin menghapus diskon ini?",
        type: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Ok',
        cancelButtonText: 'Cancel'
    }).then(function () {
        window.location.href = BASE_URL + 'discount/delete/' + id;
    })
}
function hapus_stok(id) {
    swal({
        title: 'Konfirmasi',
        text: "Apa anda yakin ingin menghapus stok ini?",
        type: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Ok',
        cancelButtonText: 'Cancel'
    }).then(function () {
        window.location.href = BASE_URL + 'stock/delete/' + id;
    })
}
function hapus_pengguna(id) {
    swal({
        title: 'Konfirmasi',
        text: "Apa anda yakin ingin menghapus pengguna ini?",
        type: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Ok',
        cancelButtonText: 'Cancel'
    }).then(function () {
        window.location.href = BASE_URL + 'accounts/delete/' + id;
    })
}
function hapus_cart_penerimaan(id) {
    swal({
        title: 'Konfirmasi',
        text: "Apa anda yakin ingin menghapus item ini?",
        type: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Ok',
        cancelButtonText: 'Cancel'
    }).then(function () {
        $.ajax({
            url: BASE_URL + 'product/receive/remove_cart/' + id,
            cache: false,
            success: function(html){
                //$("#keranjang-diterima").load(BASE_URL + 'product/show_cart/', init_slider);
                //$("#total-harga-diterima").load(BASE_URL + 'product/cart_total/');
                load_table_keranjang_penerimaan();
            }
        });
    })
}
function hapus_cart_pengembalian(id) {
    swal({
        title: 'Konfirmasi',
        text: "Apa anda yakin ingin menghapus item ini?",
        type: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Ok',
        cancelButtonText: 'Cancel'
    }).then(function () {
        $.ajax({
            url: BASE_URL + 'product/return/remove_cart/' + id,
            cache: false,
            success: function(html){
                load_table_keranjang_pengembalian();
            }
        });
    })
}
function get_qrcode(id) {
    $.ajax({
        url: BASE_URL + 'product/qrcode/' + id,
        cache: false,
        success: function(html){
            $("#body-qrcode").html(html);
            $('#modal-qrcode').modal('show');
        }
    });
}
function matchStart(params, data) {
  // If there are no search terms, return all of the data
  if ($.trim(params.term) === '') {
    return data;
  }

  // Skip if there is no 'children' property
  if (typeof data.children === 'undefined') {
    return null;
  }

  // `data.children` contains the actual options that we are matching against
  var filteredChildren = [];
  $.each(data.children, function (idx, child) {
    if (child.text.toUpperCase().indexOf(params.term.toUpperCase()) == 0) {
      filteredChildren.push(child);
    }
  });

  // If we matched any of the timezone group's children, then set the matched children on the group
  // and return the group object
  if (filteredChildren.length) {
    var modifiedData = $.extend({}, data, true);
    modifiedData.children = filteredChildren;

    // You can return modified objects from here
    // This includes matching the `children` how you want in nested data sets
    return modifiedData;
  }

  // Return `null` if the term should not be displayed
  return null;
}