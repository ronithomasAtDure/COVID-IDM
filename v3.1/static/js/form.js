class form {
  constructor(param) {
    this.statedata = null;
    this.districtlist = null;
  }

  init() {
    console.log('form init')
    //this.getStateData();
    this.applyIronSlider();
    this.datePickerevent();
    this.onFormSubmit()
    this.onIntervatinCheckbox()
    this.onPopulRadioClick()
    this.onPoulationInput()
  }

  datePickerevent() {

    $("#inputfdd").datepicker({
      format: 'yyyy-mm-dd',
      autoclose: true
    })

    $(".ed").datepicker({
      format: 'yyyy-mm-dd',
      autoclose: true
    })

   

    $(".sd").datepicker({
      format: 'yyyy-mm-dd',
      autoclose: true
    }).on('changeDate', function (selected) {
      var startDate = new Date(selected.date.valueOf());

      $('#lockdownlift, #stratscaledate').datepicker('setStartDate', startDate);
    });

    
    $(".fpdCalender").datepicker({
      format: 'yyyy-mm-dd',
      autoclose: true
    }).on('changeDate', function (selected) {
      var startDate = new Date(selected.date.valueOf());

      $('#lockdownlift, #stratscaledate').datepicker('setStartDate', startDate);
    });

    $(".fpd").datepicker({
      format: 'yyyy-mm-dd',
      autoclose: true
    })

    $(".fvd").datepicker({
      format: 'yyyy-mm-dd',
      yearRange: '2021:250',
      autoclose: true
    })

    $(".vsd").datepicker({
      format: 'yyyy-mm-dd',
      yearRange: '2021:250',
      autoclose: true
    })
    

    // $("#inputed").datepicker({
    //   format: 'dd-mm-dd',
    //   autoclose: true
    // }).on('changeDate', function (selected) {
    //   var startDate = new Date(selected.date.valueOf());

    //   $('#lockdownlift, #stratscaledate').datepicker('setStartDate', startDate);
    // });

    $('#lockdownlift, #stratscaledate').datepicker({
      format: 'yyyy-mm-dd',
      autoclose: true,
    }).on("changeDate", function (selected) {
      var startDate = new Date(selected.date.valueOf());
      $('#inputsd').datepicker('setEndDate', startDate);
    });
  }

  applyIronSlider() {
    var that = this;
    $("#inputelslider,#inputscslider,#inputacslider").ionRangeSlider({
      min: 0,
      grid: false,
      max: 100,
      from: 0,
      onChange: function (data) {
        that.fillSliderinputVal(data)
      },
    });
    $("#inputadqslider").ionRangeSlider({
      min: 1,
      grid: false,
      max: 100,
      from: 0,
      onChange: function (data) {
        that.fillSliderinputVal(data)
      },
    });
    //   $("#inputpopslider").ionRangeSlider({
    //     min: 1000,
    //     grid: false,
    //     prettify_enabled: true,
    //     prettify_separator: ",",
    //     max: 10000000,
    //     from: 0,
    //     onChange: function (data) {
    //       that.fillSliderinputVal(data)
    //     },
    //   });
    $("#inputpsslider").ionRangeSlider({
      type: "double",
      min: 0,
      grid: false,
      max: 100,
      from: 20,
      to: 70,
      onChange: function (data) {
        var v = parseInt($('#inputps').val());
        var from = data.from;
        var to = data.to;
        if (!isNaN(v)) {
          that.calPopDistributionVal(v, from, to)
        }

        //that.fillSliderinputVal(data)
      },
    });

    $("#inputrpslider").ionRangeSlider({
      min: 1,
      grid: false,
      step: 0.1,
      max: 6,
      from: 1,
      onChange: function (data) {
        that.fillSliderinputVal(data)
      },
    });
    $("#inputhbcslider").ionRangeSlider({
      min: 0,
      grid: false,
      prettify_enabled: true,
      prettify_separator: ",",
      max: 1000000,
      from: 0,
      onChange: function (data) {
        that.fillSliderinputVal(data)
      },
    });
    $("#inputhpopslider").ionRangeSlider({
      min: 1000,
      step: 1,
      grid: false,
      prettify_enabled: true,
      prettify_separator: ",",
      max: 2000000,
      from: document.getElementById('inputhpop').value,
      onChange: function (data) {
        that.fillSliderinputVal(data)
      },
    });
    $("#inputhb1slider").ionRangeSlider({
      min: 1.02,
      grid: false,
      step: 0.001,
      max: 6,
      from: document.getElementById('inputhb1').value,
      onChange: function (data) {
        that.fillSliderinputVal(data)
      },
    });

    $("#inputhb2slider").ionRangeSlider({
      min: 1.02,
      grid: false,
      step: 0.001,
      max: 6,
      from: document.getElementById('inputhb2').value,
      onChange: function (data) {
        that.fillSliderinputVal(data)
      },
    });

    $("#inputhb3slider").ionRangeSlider({
      min: 1.02,
      grid: false,
      step: 0.001,
      max: 6,
      from: document.getElementById('inputhb3').value,
      onChange: function (data) {
        that.fillSliderinputVal(data)
      },
    });
    $("#inputhwaslider").ionRangeSlider({
      min: 4,
      grid: false,
      step: 1,
      max: 24,
      from: document.getElementById('inputhwa').value,
      onChange: function (data) {
        that.fillSliderinputVal(data)
      },
    });
    $("#inputhieslider").ionRangeSlider({
      min: 0,
      grid: false,
      step: 0.01,
      max: 100,
      from: document.getElementById('inputhie').value,
      onChange: function (data) {
        that.fillSliderinputVal(data)
      },
    });
    $("#inputpdslider").ionRangeSlider({
      min: 0,
      grid: false,
      step: 0.01,
      max: 200,
      from: document.getElementById('inputpd').value,
      onChange: function (data) {
        that.fillSliderinputVal(data)
      },
    });
    $("#inputhtpslider").ionRangeSlider({
      min: 1,
      grid: false,
      step: 0.0001,
      max: 6,
      from: 4,
      onChange: function (data) {
        that.fillSliderinputVal(data)
      },
    });
    $("#inputhspslider").ionRangeSlider({
      min: 0,
      grid: false,
      step: 0.01,
      max: 100,
      from: 7.1,
      onChange: function (data) {
        that.fillSliderinputVal(data)
      },
    });
    $("#inputhdtpslider").ionRangeSlider({
      min: 0,
      grid: false,
      step: 10,
      max: 500,
      from: 232,
      onChange: function (data) {
        that.fillSliderinputVal(data)
      },
    });
    // $("#inputhd1slider").ionRangeSlider({
    //   min: 0,
    //   grid: false,
    //   step: 1,
    //   max: 12,
    //   from: document.getElementById('inputhd1').value,
    //   onChange: function (data) {
    //     that.fillSliderinputVal(data)
    //   },
    // });
    // $("#inputhd2slider").ionRangeSlider({
    //   min: 0,
    //   grid: false,
    //   step: 1,
    //   max: 12,
    //   from: document.getElementById('inputhd2').value,
    //   onChange: function (data) {
    //     that.fillSliderinputVal(data)
    //   },
    // });
    $("#inputhvrslider").ionRangeSlider({
      min: 0,
      grid: false,
      step: 0.01,
      max: 100,
      from: document.getElementById('inputhvr').value,
      onChange: function (data) {
        that.fillSliderinputVal(data)
      },
    });
    $("#inputhvdslider").ionRangeSlider({
      min: 0,
      grid: false,
      step: 1,
      max: 12,
      from: document.getElementById('inputhvd').value,
      onChange: function (data) {
        that.fillSliderinputVal(data)
      },
    });
    $("#inputhldslider").ionRangeSlider({
      min: 0,
      grid: false,
      step: 1,
      max: 365,
      from: 0,
      onChange: function (data) {
        that.fillSliderinputVal(data)
      },
    });
    $("#inputhpcslider").ionRangeSlider({
      min: 0,
      grid: false,
      step: 0.11,
      max: 100,
      from: document.getElementById('inputhpc').value,
      onChange: function (data) {
        that.fillSliderinputVal(data)
      },
    });
    $("#inputhelslider").ionRangeSlider({
      min: 0,
      grid: false,
      step: 0.11,
      max: 100,
      from: document.getElementById('inputhel').value,
      onChange: function (data) {
        that.fillSliderinputVal(data)
      },
    });

    $('.sliderval').on('keyup mouseup', function () {
      var v = parseInt($(this).val());
      var min = parseInt($(this).attr('min'));
      var max = parseInt($(this).attr('max'));
      if (v > max) {
        v = max
        $(this).val(max);
      }

      if (v < 0) {
        v = 0
        $(this).val(0);
      }
      that.addSliderVal(this, v)
    })

  }

  onPoulationInput() {
    var that = this
    $('#inputps').on('keyup mouseup', function () {
      var v = parseInt($(this).val());
      if (v < 0) {
        v = 0
        $(this).val(0);
      }
      var slider = $("#inputpsslider").data("ionRangeSlider");
      var from = slider.result.from;
      var to = slider.result.to;
      that.calPopDistributionVal(v, from, to)
    })

    $('.popVal').on('keyup mouseup', function () {
      var v = parseInt($(this).val());
      if (v < 0 || isNaN(v)) {
        v = 0
        $(this).val(0);
        return false
      }
      that.childrendpopTomainpop()
    })

  }

  childrendpopTomainpop(v) {
    var pop15 = parseInt($('.pop15').val());
    var pop15to64 = parseInt($('.pop15to64').val());
    var pop65 = parseInt($('.pop65').val());

    var total = pop15 + pop15to64 + pop65
    $('.totalPop').val(total);

    var from = pop15 / total * 100;
    var to = pop65 == 0 ? 100 : from + (pop15to64 / total * 100);
    var slider = $("#inputpsslider").data("ionRangeSlider");
    slider.update({
      from: from,
      to: to,
    });

  }

  calPopDistributionVal(v, from, to) {
    //console.log(v,from, to)
    var diff = to - from;
    var lstdiff = 100 - to
    var pop15 = from / 100 * v;
    var pop15to64 = diff / 100 * v;
    var pop65 = lstdiff / 100 * v;
    $('.pop15').val(parseInt(pop15));
    $('.pop15to64').val(parseInt(pop15to64));
    $('.pop65').val(parseInt(pop65));
  }

  addSliderVal(ref, v) {
    var $range = $(ref).closest('.sliderContainer').find('.inputslider')
    var range = $range.data("ionRangeSlider");
    range.update({
      from: v,
    });
  }

  fillSliderinputVal(data) {
    var val = data.from;
    var ref = data.input[0]
    $(ref).closest('.sliderContainer').find('.sliderval').val(val)
  }

  getStateData() {
    //    var that = this
    //    $.getJSON("assest/data/state.json", function (json) {
    //      console.log(json);
    //      that.statedata = json;
    //      that.renderState(json)
    //    });
    api.getLocation(this, this.renderState)
  }

  renderState(ref, data) {
    console.log(data)
    console.log(ref)
    ref.statedata = data;
    var option = '';
    for (var i = 0; i < data.length; i++) {
      option += '<option value="' + data[i]['name'] + '">' + data[i]['name'] + '</option>'
    }
    $('#stateSelect').html('')
    $('#stateSelect').append(option)
    ref.onstatselect()
    ref.renderDistricts($('#stateSelect').val())
  }

  onstatselect() {
    $('#stateSelect').off().on('change', function () {
      //totalPop
    })
  }

  onIntervatinCheckbox() {
    $('#interventionChecbox').off().on('change', function () {
      if ($(this).is(':checked')) {
        dashboardChartsClass.renderwith_withoudIterventionChart()
      } else {
        dashboardChartsClass.renderwithinterventionChart()
      }
    })
  }

  onPopulRadioClick() {
    var that = this
    $('.popradio').off().on('click', function () {
      var val = $(this).val()
      if (val == 2) {
        $('.popVal').val('')
      } else {
        that.renderPopulations($('#districtSelect').val())
      }
    })
  }

  renderDistricts(stateid) {
    console.log(this.statedata)
    var distdata = this.statedata.filter(obj => obj.name == stateid)
    var Districtlist = distdata[0].districts
    this.districtlist = Districtlist;
    var option = '';
    for (var i = 0; i < Districtlist.length; i++) {
      option += '<option value="' + Districtlist[i]['districtid'] + '">' + Districtlist[i]['name'] + '</option>'
    }
    $('#districtSelect').html('')
    $('#districtSelect').append(option)
    this.ondistrictChange()
    this.renderPopulations($('#districtSelect').val())
  }
  ondistrictChange() {
    var that = this;
    $('#districtSelect').off().on('change', function () {
      var val = $(this).val()
      that.renderPopulations(val)
    })
  }
  renderPopulations(distId) {
    var distObj = this.districtlist.filter(obj => obj.districtid == distId)
    if (distObj.length > 0) {
      var pop15 = parseInt(distObj[0].ageGrpRecords[0]["total"].replace(/,/g, ''))
      var pop15to64 = parseInt(distObj[0].ageGrpRecords[1]["total"].replace(/,/g, ''))
      var pop65 = parseInt(distObj[0].ageGrpRecords[2]["total"].replace(/,/g, ''))
      $('.pop15').val(pop15);
      $('.pop15to64').val(pop15to64);
      $('.pop65').val(pop65);
      $('.totalPop').val(pop65 + pop15to64 + pop65);
    }
  }

  onFormSubmit() {
    var that = this
    var numberKey = ['R0', 'HospitalBedCapacity', 'TotalPopulation', 'Children_15', 'Adults_19_64', 'Elderly_65', 'C', 'AverageDelay', 'p_qur', 'q_asym_ratio']
    var datekeys = ['LockdownReleaseDate', 'LockdownStartDate', 'QuarantineStartDate']
    var percantagekeys = ['C', 'p_qur', 'q_asym_ratio']
    $('#submitBtn').off().on('click', function (e) {
      e.preventDefault()
      dashboardChartsClass.interventionFlag = true
      $('.daterror').addClass('hide')
      var $form = $("#inputform");
      var data = that.getFormData($form);
      var flag = that.formValidations(data);
      console.log(dashboardChartsClass.interventionFlag)
      numberKey.forEach(obj => {
        if (data[obj] != "") {
          data[obj] = parseFloat(data[obj])
        }
      })

      percantagekeys.forEach(obj => {
        data[obj] = data[obj] / 100
      })

      console.log(data)
      if (flag) {
        data['functionalname'] = "responsejson.py";
        that.callChatApi(data)
      } else {
        $('.daterror').removeClass('hide')
      }
    })
  }

  formValidations(data) {
    var mandtorFileds = ['TotalPopulation', 'Children_15', 'Adults_19_64', 'Elderly_65', 'FirstDateOfDeath']

    var flag = true;
    mandtorFileds.forEach(obj => {
      if (data[obj] === "") {
        $('.daterror').text('Please fill demographic parameters')
        flag = false;
      }
    })

    if (data["LockdownStartDate"] === "" && data["QuarantineStartDate"] === "") {
      dashboardChartsClass.interventionFlag = false
      //$('.daterror').text('Please fill Intervention Scenarios or Quarantining Strategies')
      //flag = false;
    }

    if (data["LockdownStartDate"] != "" && data["LockdownReleaseDate"] === "") {
      $('.daterror').text('Please add release date')
      flag = false;
    }

    if (data["LockdownStartDate"] != "" && data["LockdownReleaseDate"] != "") {
      $('.lockdownLable').removeClass('hide')
    } else {
      $('.lockdownLable').addClass('hide')
    }

    if (data["QuarantineStartDate"] != "") {
      $('.quarantineLable').removeClass('hide')
    } else {
      $('.quarantineLable').addClass('hide')
    }

    return flag
  }

  getFormData($form) {
    var unindexed_array = $form.serializeArray();
    var indexed_array = {};
    $.map(unindexed_array, function (n, i) {
      indexed_array[n['name']] = n['value'];
    });
    return indexed_array;
  }

  callChatApi(params) {
    $('.chartCard .card-body').waitMe({ 'text': 'Fetching charts data', bg: '#fff' });
    api.getChartData(params)
  }
}

var formclass = new form()
formclass.init()

$(function () {
  $("#wanning").on("click", function () {
    $(".answer").toggle(this.checked);
  });
});

// date validate

$("#inputfpd, #inputfvd").datepicker({
  format: 'yyyy-mm-dd'
});

$("#inputfvd").change(function () {
    var startDate = document.getElementById("inputfpd").value;
    var endDate = document.getElementById("inputfvd").value;
 
    if ((Date.parse(endDate) <= Date.parse(startDate))) {
        alert("Future variant date should be later than the Second peak date");
        document.getElementById("inputfvd").value = "";
    }
});

$("#inputsd, #inputed").datepicker({
  format: 'yyyy-mm-dd'
});

$("#inputed").change(function () {
    var startDate = document.getElementById("inputsd").value;
    var endDate = document.getElementById("inputed").value;
 
    if ((Date.parse(endDate) <= Date.parse(startDate))) {
        alert("Lockdown End date should be greater than Lockdown Start date");
        document.getElementById("inputed").value = "";
    }
});

$("#inputhwa").change(function () {
  var wa = document.getElementById("inputhwa").value;

  if ((wa < 3)) {
      alert("Wanning greater than or equal to 4");
      document.getElementById("inputhwa").value = "";
  }
});

$("#inputfvd").change(function () {
  var startDate = "2021-05-31";
  var endDate = document.getElementById("inputfvd").value;

  if ((Date.parse(endDate) <= Date.parse(startDate))) {
      alert("Future Variant date to be later than 2021-05-31");
      document.getElementById("inputed").value = "";
  }
});

$(function () {
  $("#popden").on("click", function () {
    $(".answer-1").toggle(this.checked);
  });
});

function printDiv(divName) {
  var printContents = document.getElementById(divName).innerHTML;
  var originalContents = document.body.innerHTML;

  document.body.innerHTML = printContents;

  window.print();

  document.body.innerHTML = originalContents;
}

const printPDF = () => {
  // document
  //   .getElementById("pdf_download_alert")
  //   .classList.replace("hide", "show");
  //document.getElementById("Col_Desc").classList.remove("colb-desp-summary");
  //document.getElementById("Col_Desc").style.maxHeight = "100px";

  const domElement = document.getElementById("printableArea");
  html2canvas(domElement, {
    //  allowTaint: true,
    useCORS: true,
  }).then((canvas) => {
   
    const domElement1 = document.getElementById("footer-about");
    html2canvas(domElement1, {
      //  allowTaint: true,
      useCORS: true,
    }).then((canvas1) => {
    
        const pdf = new jsPDF("landscape");
        // var width = ImplPartnerDoc.scrollWidth;;
        // var height = ImplPartnerDoc.scrollHeight;
        // console.log(width);
        // console.log(height);
        let ScreenshotAttachment = canvas.toDataURL();
        let ScreenshotAttachment1 = canvas1.toDataURL();
        pdf.addImage(ScreenshotAttachment, "JPEG", 0, 20, 297, 0);
        // pdf.addPage();
        pdf.addImage(ScreenshotAttachment1, "JPEG", 0, 200, 297, 0);
        // pdf.addPage();
        // pdf.addImage(partnerDataURL, "JPEG", 5, 5, 180, 100);

        let pdfsave = document.getElementById('place').value + " " + "CHROMIC Simulation.pdf";
        pdf.save(pdfsave);
        // document
        //   .getElementById("pdf_download_alert")
        //   .classList.replace("show", "hide");
      });
    });
};

const printPDF1 = () => {
  // document
  //   .getElementById("pdf_download_alert")
  //   .classList.replace("hide", "show");
  //document.getElementById("Col_Desc").classList.remove("colb-desp-summary");
  //document.getElementById("Col_Desc").style.maxHeight = "100px";

  const domElement = document.getElementById("p1");
  html2canvas(domElement, {
    //  allowTaint: true,
    useCORS: true,
  }).then((canvas) => {
   
    html2canvas(descDomElement, {
      //  allowTaint: true,
      useCORS: true,
    }).then((descCanvas) => {
      let ScreenshotAttachment = canvas.toDataURL();
      let descDataURL = descCanvas.toDataURL();
      document
        .getElementById("Col_Desc")
        .classList.add("colb-desp-summary-height");
      //document.getElementById("Col_Desc").style.maxHeight = "150px";
      //console.log("File: ", ScreenshotAttachment);
      document
        .getElementById("ImplPartner")
        .classList.remove("partners_content");
      const ImplPartnerDoc = document.getElementById("Implementing_partner");
      html2canvas(ImplPartnerDoc, {
        //  allowTaint: true,
        useCORS: true,
      }).then((partnerCanvas) => {
        let partnerDataURL = partnerCanvas.toDataURL();
        document
          .getElementById("ImplPartner")
          .classList.add("partners_content");
        const pdf = new jsPdf();
        // var width = ImplPartnerDoc.scrollWidth;;
        // var height = ImplPartnerDoc.scrollHeight;
        // console.log(width);
        // console.log(height);
        pdf.addImage(ScreenshotAttachment, "JPEG", 5, 5, 200, 280);
        pdf.addPage();
        pdf.addImage(descDataURL, "JPEG", 5, 5, 200, 160);
        pdf.addPage();
        pdf.addImage(partnerDataURL, "JPEG", 5, 5, 180, 100);

        let pdfsave = props.getProgram + ".pdf";
        pdf.save(pdfsave);
        document
          .getElementById("pdf_download_alert")
          .classList.replace("show", "hide");
      });
      // pdf.addImage(descDataURL, "JPEG", 5, 5, 200, 210);

      // let pdfsave = props.getProgram + ".pdf";
      // pdf.save(pdfsave);
    });
  });
};

function goBack() {
  window.history.back();
}