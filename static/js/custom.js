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
             { orderable: false, targets: [-1] }
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