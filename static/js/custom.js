var current_pathname = window.location.pathname;
$(document).ready(function() {
    var is_update = false;
    var can_update_slide = true;
    //$("#keranjang-diterima").load(BASE_URL + 'product/show_cart/', init_slider);
    init_daterangepicker();
    init_daterangepicker_transaksi();
    if(current_pathname.search(/customer_return/i) > 0) {
        load_table_keranjang_retur();
    } else if(current_pathname.search(/receive/i) > 0) {
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
            if($(this).data('prev') >= $(this).val()) {
                var zzz = $(this).data('prev') - $(this).val();
                $('.sisa-' + $(this).data('pk')).text(sisa + zzz);
                $('#txt-sisa-' + pk).val(sisa + zzz);
            } else {
                var zzz =  $(this).val() - $(this).data('prev');
                var max = prev + sisa;
                if(sisa - zzz <= 0) {
                    $('.sisa-' + $(this).data('pk')).text(0);
                    $('#txt-sisa-' + pk).val(0);
                    is_update = true;
                    can_update_slide = false;
                    update_slider2($(this), {'from': max});
                } else {
                    $('.sisa-' + $(this).data('pk')).text(sisa - zzz);
                    $('#txt-sisa-' + pk).val(sisa - zzz);
                }
            }
            $('.stock-input-' + pk + '-' + a[2]).val($(this).val());
            $(this).data('prev', $(this).val());
            /*if((sisa - ($(this).val() - prev) >= 0) && ($(this).val() != prev)) {
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
            }*/
        }
    });

    $('#mapping-gudang').on('keyup keypress blur change', 'input[class*="stock-slider3-"]', function(event) {
        if(can_update_slide) {
            var pk = $(this).data('pk');
            var sisa = parseInt($('.sisa-' + pk).text());
            var prev = parseInt($(this).data('prev'));
            var patt = /stock-slider3-([0-9+])-([0-9+])/i;
            var a = $(this).attr('class').match(patt);

            if($(this).data('prev') >= $(this).val()) {
                var zzz = $(this).data('prev') - $(this).val();
                $('.sisa-' + $(this).data('pk')).text(sisa + zzz);
                $('#txt-sisa-' + pk).val(sisa + zzz);
            } else {
                var zzz =  $(this).val() - $(this).data('prev');
                var max = prev + sisa;
                if(sisa - zzz <= 0) {
                    $('.sisa-' + $(this).data('pk')).text(0);
                    $('#txt-sisa-' + pk).val(0);
                    is_update = true;
                    can_update_slide = false;
                    update_slider2($(this), {'from': max});
                } else {
                    $('.sisa-' + $(this).data('pk')).text(sisa - zzz);
                    $('#txt-sisa-' + pk).val(sisa - zzz);
                }
            }
            $('.stock-input-' + pk + '-' + a[2]).val($(this).val());
            $(this).data('prev', $(this).val());
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

    function update_slider2(elem, val) {
        if(is_update) {
            var slider = elem.data("ionRangeSlider");
            slider.update(val);
            is_update = false;
            can_update_slide = true;
        }
    }

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
            //load_table_keranjang_penerimaan();
            
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

    $('#mapping-gudang').on('click', '.tambah-gudang-penerimaan', function() {
        $('#select-tambah-gudang').html('');
        $('#modal-tambah-gudang').modal('show');
        $('#text-tambah-gudang').text('Menambah Gudang untuk Produk ' + $(this).data('namaproduk'));
        var produk_id = $(this).data('produk');
        $('#form-tambah-gudang').html('<select class="form-control" id="select-tambah-gudang" name="warehouse[' + produk_id + ']"></select>');
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
        console.log($("form#form-keranjang-penerimaan").serialize());
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
                var data = $("form#form-keranjang-penerimaan").serialize();
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
        /*if(parseInt(elem.text()) > 0) {
            swal(
              'Oops...',
              'Masih ada produk yang mempunyai sisa stok',
              'error'
            );
        } else {
        */
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
        //}
    });



    /* Retur */
    $('#btn-cari-invoice').click(function() {
        var invoice_number = $('#invoice_number').val();
        $.ajax({
            url: BASE_URL + 'customer_return/get_invoice/' + invoice_number,
            cache: false,
            success: function(res){
                if(res == 'error') {
                    swal(
                      'Oops...',
                      'No Invoice tidak valid',
                      'error'
                    );
                } else {
                    load_table_keranjang_retur();
                    init_slider();
                }
            }
        });
    });
    $('.submit-keranjang-retur').click(function() {
        var punya_sisa = false;
        var elem = '';
        var sum = 0;
        $('#mapping-gudang span[class*="sisa"]').each(function(i, el){
            elem = $(el);
            sum = sum + parseInt(elem.text());
        });
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
            var data = $("form#form-keranjang-penerimaan").serialize() + '&invoice_number=' + $('#invoice_number').val();
            $.ajax({
                type: "POST",
                url: BASE_URL + 'customer_return/testpost/',
                data: $("form#form-keranjang-penerimaan").serialize(),
                cache: false,
                success: function(res){
                    $.ajax({
                        type: "POST",
                        url: BASE_URL + 'customer_return/checkout/',
                        data: data,
                        cache: false,
                        success: function(res){
                            swal(
                              'Success',
                              'Berhasil mengembalikan produk!',
                              'success'
                            )
                            $.ajax({
                                url: BASE_URL + 'customer_return/show_cart/',
                                cache: false,
                                success: function(res){
                                    $("#mapping-gudang").html($(res));
                                    init_slider();
                                }
                            });
                            $("#total-harga-diterima").load(BASE_URL + 'customer_return/cart_total/');
                        }
                    });
                }
            });
        });
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
    $('#mapping-gudang input[class*="stock-slider3-"]').each(function(i, el){
        var prev = parseInt($(this).data('prev'));
        var patt = /stock-slider3-([0-9+])-/i;
        var a = $(this).attr('class').match(patt);
        var pk = a[1]
        var sisa = parseInt($('.sisa-' + pk).text());
        var qty = parseInt($('#qty-' + pk).val());
        $('.' + el.className).ionRangeSlider({
            min:0,
            max: qty
        });

    });
}
function load_table_keranjang_retur() {
    $.ajax({
        type: "POST",
        url: BASE_URL + 'customer_return/testpost/',
        data: $("form#form-keranjang-penerimaan").serialize(),
        cache: false,
        success: function(res){
            $.ajax({
                url: BASE_URL + 'customer_return/show_cart/',
                cache: false,
                success: function(res){
                    $("#mapping-gudang").html($(res));
                    init_slider();
                }
            });
            //$("#keranjang-diterima").load(BASE_URL + 'product/show_cart/', init_slider);
            $("#total-harga-diterima").load(BASE_URL + 'customer_return/cart_total/');
            //init_slider();
        }
    });
    //("#keranjang-diterima").load(BASE_URL + 'product/show_cart/', init_slider);
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
function loading() {
  return '<div class="text-center"><img src="' + BASE_URL + 'static/images/loading.gif"/></div>';
}
function beep() {
    var snd = new Audio(BASE_URL + 'static/Beep2.ogg');
    snd.volume = 1.0;
    snd.play();
}
function init_daterangepicker_transaksi() {

    if( typeof ($.fn.daterangepicker) === 'undefined'){ return; }
    console.log('init_daterangepicker');

    var cb = function(start, end, label) {
      console.log(start.toISOString(), end.toISOString(), label);
      $('#reportrange-transaksi span').html(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'));
    };
    var daftar_transaksi = $('#daftar-transaksi').dataTable({
        "processing": true,
        "serverSide": true,
        "ajax": BASE_URL + 'transaction/data/?start_date=' + moment().subtract(29, 'days').format('YYYY-MM-DD') + '&end_date=' + moment().format('YYYY-MM-DD'),
        columnDefs: [
             { orderable: false, targets: [-1] }
        ]
    });
    var optionSet1 = {
      startDate: moment().subtract(7, 'days'),
      endDate: moment(),
      maxDate: moment(),
      /*dateLimit: {
        days: 60
      },*/
      showDropdowns: true,
      showWeekNumbers: true,
      timePicker: false,
      timePickerIncrement: 1,
      timePicker12Hour: true,
      ranges: {
        'Today': [moment(), moment()],
        'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
        'Last 7 Days': [moment().subtract(6, 'days'), moment()],
        'Last 30 Days': [moment().subtract(29, 'days'), moment()],
        'This Month': [moment().startOf('month'), moment().endOf('month')],
        'Last Month': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
      },
      opens: 'left',
      buttonClasses: ['btn btn-default'],
      applyClass: 'btn-small btn-primary',
      cancelClass: 'btn-small',
      format: 'MM/DD/YYYY',
      separator: ' to ',
      locale: {
        applyLabel: 'Submit',
        cancelLabel: 'Clear',
        fromLabel: 'From',
        toLabel: 'To',
        customRangeLabel: 'Custom',
        daysOfWeek: ['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa'],
        monthNames: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
        firstDay: 1
      }
    };

    $('#reportrange-transaksi span').html(moment().subtract(29, 'days').format('MMMM D, YYYY') + ' - ' + moment().format('MMMM D, YYYY'));
    $('#reportrange-transaksi').daterangepicker(optionSet1, cb);
    $('#reportrange-transaksi').on('show.daterangepicker', function(ev, picker) {
      console.log("show event fired");
    });
    $('#reportrange-transaksi').on('hide.daterangepicker', function() {
      console.log("hide event fired");
    });
    $('#reportrange-transaksi').on('apply.daterangepicker', function(ev, picker) {
        daftar_transaksi.api().ajax.url(BASE_URL + 'transaction/data/?start_date=' + picker.startDate.format('YYYY-MM-DD') + '&end_date=' + picker.endDate.format('YYYY-MM-DD')).load();
       console.log("apply event fired, start/end dates are " + picker.startDate.format('YYYY-MM-DD') + " to " + picker.endDate.format('YYYY-MM-DD'));
    });
    $('#reportrange-transaksi').on('cancel.daterangepicker', function(ev, picker) {
      console.log("cancel event fired");
    });
    $('#options1').click(function() {
      $('#reportrange-transaksi').data('daterangepicker').setOptions(optionSet1, cb);
    });
    $('#options2').click(function() {
      $('#reportrange-transaksi').data('daterangepicker').setOptions(optionSet2, cb);
    });
    $('#destroy').click(function() {
      $('#reportrange-transaksi').data('daterangepicker').remove();
    });
}

function init_daterangepicker() {

    if( typeof ($.fn.daterangepicker) === 'undefined'){ return; }
    console.log('init_daterangepicker');

    var cb = function(start, end, label) {
      console.log(start.toISOString(), end.toISOString(), label);
      $('#reportrange span').html(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'));
    };

    var optionSet1 = {
      startDate: moment().subtract(7, 'days'),
      endDate: moment(),
      maxDate: moment(),
      /*dateLimit: {
        days: 60
      },*/
      showDropdowns: true,
      showWeekNumbers: true,
      timePicker: false,
      timePickerIncrement: 1,
      timePicker12Hour: true,
      ranges: {
        'Today': [moment(), moment()],
        'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
        'Last 7 Days': [moment().subtract(6, 'days'), moment()],
        'Last 30 Days': [moment().subtract(29, 'days'), moment()],
        'This Month': [moment().startOf('month'), moment().endOf('month')],
        'Last Month': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
      },
      opens: 'left',
      buttonClasses: ['btn btn-default'],
      applyClass: 'btn-small btn-primary',
      cancelClass: 'btn-small',
      format: 'MM/DD/YYYY',
      separator: ' to ',
      locale: {
        applyLabel: 'Submit',
        cancelLabel: 'Clear',
        fromLabel: 'From',
        toLabel: 'To',
        customRangeLabel: 'Custom',
        daysOfWeek: ['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa'],
        monthNames: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
        firstDay: 1
      }
    };
    if($('#mainb').length){load_chart(moment().subtract(29, 'days').format('YYYY-MM-DD'), moment().format('YYYY-MM-DD'));}
    $('#reportrange span').html(moment().subtract(29, 'days').format('MMMM D, YYYY') + ' - ' + moment().format('MMMM D, YYYY'));
    $('#reportrange').daterangepicker(optionSet1, cb);
    $('#reportrange').on('show.daterangepicker', function(ev, picker) {
      console.log("show event fired");
    });
    $('#reportrange').on('hide.daterangepicker', function() {
      console.log("hide event fired");
    });
    $('#reportrange').on('apply.daterangepicker', function(ev, picker) {
        if ($('#mainb').length){load_chart(picker.startDate.format('YYYY-MM-DD'), picker.endDate.format('YYYY-MM-DD'));}
        console.log("apply event fired, start/end dates are " + picker.startDate.format('YYYY-MM-DD') + " to " + picker.endDate.format('YYYY-MM-DD'));
    });
    $('#reportrange').on('cancel.daterangepicker', function(ev, picker) {
      console.log("cancel event fired");
    });
    $('#options1').click(function() {
      $('#reportrange').data('daterangepicker').setOptions(optionSet1, cb);
    });
    $('#options2').click(function() {
      $('#reportrange').data('daterangepicker').setOptions(optionSet2, cb);
    });
    $('#destroy').click(function() {
      $('#reportrange').data('daterangepicker').remove();
    });
}

var theme = {
color: [
  '#26B99A', '#34495E', '#BDC3C7', '#3498DB',
  '#9B59B6', '#8abb6f', '#759c6a', '#bfd3b7'
],
title: {
  itemGap: 8,
  textStyle: {
      fontWeight: 'normal',
      color: '#408829'
  }
},
markPoint: {
    label: {
        normal: {
            textStyle: {
                color: "#ffffff"
            }
        },
        emphasis: {
            textStyle: {
                color: "#000000"
            }
        }
    }
},
dataRange: {
  color: ['#1f610a', '#97b58d']
},

toolbox: {
  color: ['#408829', '#408829', '#408829', '#408829']
},

tooltip: {
  backgroundColor: 'rgba(0,0,0,0.5)',
  axisPointer: {
      type: 'line',
      lineStyle: {
          color: '#408829',
          type: 'dashed'
      },
      crossStyle: {
          color: '#408829'
      },
      shadowStyle: {
          color: 'rgba(200,200,200,0.3)'
      }
  }
},

dataZoom: {
  dataBackgroundColor: '#eee',
  fillerColor: 'rgba(64,136,41,0.2)',
  handleColor: '#408829'
},
grid: {
  borderWidth: 0
},

categoryAxis: {
  axisLine: {
      lineStyle: {
          color: '#408829'
      }
  },
  splitLine: {
      lineStyle: {
          color: ['#eee']
      }
  }
},

valueAxis: {
  axisLine: {
      lineStyle: {
          color: '#408829'
      }
  },
  splitArea: {
      show: true,
      areaStyle: {
          color: ['rgba(250,250,250,0.1)', 'rgba(200,200,200,0.1)']
      }
  },
  splitLine: {
      lineStyle: {
          color: ['#eee']
      }
  }
},
timeline: {
  lineStyle: {
      color: '#408829'
  },
  controlStyle: {
      normal: {color: '#408829'},
      emphasis: {color: '#408829'}
  }
},

k: {
  itemStyle: {
      normal: {
          color: '#68a54a',
          color0: '#a9cba2',
          lineStyle: {
              width: 1,
              color: '#408829',
              color0: '#86b379'
          }
      }
  }
},
map: {
  itemStyle: {
      normal: {
          areaStyle: {
              color: '#ddd'
          },
          label: {
              textStyle: {
                  color: '#c12e34'
              }
          }
      },
      emphasis: {
          areaStyle: {
              color: '#99d2dd'
          },
          label: {
              textStyle: {
                  color: '#c12e34'
              }
          }
      }
  }
},
force: {
  itemStyle: {
      normal: {
          linkStyle: {
              strokeColor: '#408829'
          }
      }
  }
},
chord: {
  padding: 4,
  itemStyle: {
      normal: {
          lineStyle: {
              width: 1,
              color: 'rgba(128, 128, 128, 0.5)'
          },
          chordStyle: {
              lineStyle: {
                  width: 1,
                  color: 'rgba(128, 128, 128, 0.5)'
              }
          }
      },
      emphasis: {
          lineStyle: {
              width: 1,
              color: 'rgba(128, 128, 128, 0.5)'
          },
          chordStyle: {
              lineStyle: {
                  width: 1,
                  color: 'rgba(128, 128, 128, 0.5)'
              }
          }
      }
  }
},
gauge: {
  startAngle: 225,
  endAngle: -45,
  axisLine: {
      show: true,
      lineStyle: {
          color: [[0.2, '#86b379'], [0.8, '#68a54a'], [1, '#408829']],
          width: 8
      }
  },
  axisTick: {
      splitNumber: 10,
      length: 12,
      lineStyle: {
          color: 'auto'
      }
  },
  axisLabel: {
      textStyle: {
          color: 'auto'
      }
  },
  splitLine: {
      length: 18,
      lineStyle: {
          color: 'auto'
      }
  },
  pointer: {
      length: '90%',
      color: 'auto'
  },
  title: {
      textStyle: {
          color: '#333'
      }
  },
  detail: {
      textStyle: {
          color: 'auto'
      }
  }
},
textStyle: {
  fontFamily: 'Arial, Verdana, sans-serif'
}
};
if ($('#mainb').length ){
  
  var echartBar = echarts.init(document.getElementById('mainb'), theme);
    function load_chart(start_date, end_date) {
        echartBar.showLoading();
        $.getJSON(BASE_URL + 'report/get_json/?start_date=' + start_date + '&end_date=' + end_date, function(res) {
          echartBar.setOption({
            title: {
              text: 'Grafik Penjualan',
              subtext: start_date + ' - ' + end_date
            },
            tooltip: {
              trigger: 'axis'
            },
            legend: {
              data: ['Uang Masuk', 'Keuntungan', 'Item Terjual']
            },
            toolbox: {
              show: true,
              feature: {
                magicType: {
                  show: true,
                  title: {
                    line: 'Line',
                    bar: 'Bar',
                    stack: 'Stack',
                    tiled: 'Tiled'
                  },
                  type: ['line', 'bar', 'stack', 'tiled']
                },
                restore: {
                  show: true,
                  title: "Restore"
                },
              }
            },
            calculable: false,
            xAxis: [{
              type: 'category',
              data: res.category
            }],
            yAxis: [{
              type: 'value'
            }],
            series: [{
              name: 'Uang Masuk',
              type: 'bar',
              data: res.uang_masuk,
              markPoint: {
                data: [{
                  type: 'max',
                  name: 'Tertinggi'
                }, {
                  type: 'min',
                  name: 'Terendah'
                }]
              },
              markLine: {
                data: [{
                  type: 'average',
                  name: 'Rata-Rata'
                }]
              }
            }, {
              name: 'Keuntungan',
              type: 'bar',
              data: res.keuntungan,
              markPoint: {
                data: [{
                  type: 'max',
                  name: 'Tertinggi'
                }, {
                  type: 'min',
                  name: 'Terendah'
                }]
              },
              markLine: {
                data: [{
                  type: 'average',
                  name: 'Rata-Rata'
                }]
              }
            }, {
              name: 'Item Terjual',
              type: 'bar',
              data: res.item,
              markPoint: {
                data: [{
                  type: 'max',
                  name: 'Tertinggi'
                }, {
                  type: 'min',
                  name: 'Terendah'
                }]
              },
              markLine: {
                data: [{
                  type: 'average',
                  name: 'Rata-Rata'
                }]
              }
            }]
          });
        });
        echartBar.hideLoading();
    }
}