$(document).ready(function() {
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
            $('#btn-mapping-gudang').removeClass('disabled');
        } else {
            $('#btn-mapping-gudang').addClass('disabled');
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
});
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