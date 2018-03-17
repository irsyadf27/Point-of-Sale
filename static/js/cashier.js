var app = new Vue({
  el: '#app',
  delimiters: ['${', '}'],
  data: {
    scanner: null,
    activeCameraId: null,
    cameras: [],
    scans: []
  },
  mounted: function () {
    var self = this;
    self.scanner = new Instascan.Scanner({ video: document.getElementById('canvas-kamera'), scanPeriod: 5 });
    self.scanner.addListener('scan', function (content, image) {
      var data = {
          'qrcode': content,
          'qty': $('#qty-product').val()
      }
      $.ajax({
          type: "POST",
          url: BASE_URL + 'cashier/add/',
          data: data,
          cache: false,
          beforeSend: function() {
              $("#table-barang-kasir").html(loading());
          },
          success: function(res){
            beep();
            $("#table-barang-kasir").load(BASE_URL + 'cashier/show_cart/');
            $('#qty-product').val(1);
          }
      });
    });
    Instascan.Camera.getCameras().then(function (cameras) {
      self.cameras = cameras;
      if (cameras.length > 0) {
        self.activeCameraId = cameras[0].id;
        self.scanner.start(cameras[0]);
      } else {
        console.error('No cameras found.');
      }
    }).catch(function (e) {
      console.error(e);
    });
  },
  methods: {
    formatName: function (name) {
      return name || '(unknown)';
    },
    selectCamera: function (camera) {
      this.activeCameraId = camera.id;
      this.scanner.start(camera);
    }
  }
});

$(document).ready(function() {
  $("#table-barang-kasir").load(BASE_URL + 'cashier/show_cart/');
  $('#qty-product').focus();
  $('#table-barang-kasir').editable({
      selector: '.txt-qty',
      success: function(response, newValue) {
          $("#table-barang-kasir").load(BASE_URL + 'cashier/show_cart/');
      }
  });
  $('#pelanggan').change(function() {
    var pk = $(this).val();
    if(pk != "") {
      $.ajax({
          type: "GET",
          url: BASE_URL + 'cashier/set_pelanggan/' + pk,
          cache: false,
      });
    }
  });
  $('#discount').change(function() {
    var pk = $(this).val();
    if(pk != "") {
      $.ajax({
          type: "GET",
          url: BASE_URL + 'cashier/set_discount/' + pk,
          cache: false,
          beforeSend: function() {
              $("#table-barang-kasir").html(loading());
          },
          success: function(res){
            $("#table-barang-kasir").load(BASE_URL + 'cashier/show_cart/');
          }
      });
    }
  });


  $('#save-tambah-pelanggan').click(function() {
    $('#modal-tambah-pelanggan').modal('hide');
    var data = $("form#form-tambah-pelanggan").serialize();
    $.ajax({
        type: "POST",
        url: BASE_URL + 'customer/create/',
        data: data,
        cache: false,
        success: function(res){
          swal(
            'Success',
            'Berhasil menambah pelanggan!',
            'success'
          )
          $('#id_name').val('');
          $('#id_address').val('');
          $('#id_address').val('');
        }
    });

  });

});
/* kasir */
$(".js-matcher-customer").select2({
    ajax: {
        url: BASE_URL + 'customer/list_json',
        dataType: 'json'
    },
    templateResult: formatOption
});
function formatOption (option) {
  var $option = $(
    '<div><strong>' + option.text + '</strong></div><div><i class="fa fa-phone"></i> ' + option.phone + '</div><div><i class="fa fa-map-marker"></i> ' + option.address + '</div>'
  );
  return $option;
};
$(".js-matcher-kasir").select2({
    ajax: {
        url: BASE_URL + 'product/list_json',
        dataType: 'json'
    },
    matcher: matchStart
});
$(".js-matcher-kasir").change(function() {
    if($(this).val()) {
        var data = {
            'produk': $(this).val(),
            'qty': $('#qty-product').val()
        }
        $.ajax({
            type: "POST",
            url: BASE_URL + 'cashier/add/',
            data: data,
            cache: false,
            beforeSend: function() {
                $("#table-barang-kasir").html(loading());
            },
            success: function(res){
              beep();
              $("#table-barang-kasir").load(BASE_URL + 'cashier/show_cart/');
              $(".js-matcher-kasir").val(null).trigger("change");
              $('#qty-product').val(1);
            }
        });
    }
});
function hapus_cart_kasir(id) {
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
            url: BASE_URL + 'cashier/remove_cart/' + id,
            cache: false,
            beforeSend: function() {
                $("#table-barang-kasir").html(loading());
            },
            success: function(html){
                $("#table-barang-kasir").load(BASE_URL + 'cashier/show_cart/');
            }
        });
    })
}