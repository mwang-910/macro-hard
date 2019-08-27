/**
 * Created by yaling.he on 2015/11/17.
 */
$(function () {
    $('.removeProvider').click(function () {
        $('.zhezhao').css('display', 'block');
        $('#removeProv').fadeIn();
    });
});

//供应商管理页面上点击删除按钮弹出删除框(providerList.html)
$(function () {
    $('.removeProvider').click(function () {
        $('.zhezhao').css('display', 'block');
        $('#removeProv').fadeIn();
    });
});

$(function () {
    $('#no').click(function () {
        $('.zhezhao').css('display', 'none');
        $('#removeProv').fadeOut();
    });
});


//订单管理页面上点击删除按钮弹出删除框(billList.html)
$(function () {
    $('.removeBill').click(function () {
        $('.zhezhao').css('display', 'block');
        $('#removeBi').fadeIn();
    });
});

$(function () {
    $('#no').click(function () {
        $('.zhezhao').css('display', 'none');
        $('#removeBi').fadeOut();
    });
});

//用户管理页面上点击删除按钮弹出删除框(userList.html)
$(function () {
    $('.removeUser').click(function () {
        $('.zhezhao').css('display', 'block');
        $('#removeUse').fadeIn();
    });
});

$(function () {
    $('#no').click(function () {
        $('.zhezhao').css('display', 'none');
        $('#removeUse').fadeOut();
    });
});

$(function() {
    $('#btnupdate').click(function () {

        var ptype=$("input[name='type']").val();
        var pnumber=$("input[name='number']").val();
        var pprice=$("input[name='price']").val();
        if(ptype==''||ptype==undefined||ptype==null){
            alert("请输入商品种类");
        }
        else if(pnumber==''||pnumber==undefined||pnumber==null){
            alert("请输入商品库存数量");
        }
        else if( pprice==''||pprice==undefined||pprice==null){
            alert("请输入商品单价");
        }
        else{
            $('#frm').submit();
            alert("修改成功");
        }
    });
});

$(function() {
    $('#btnadd').click(function () {
        var proID=$("input[name='productId']").val();
        var proName=$("input[name='productName']").val();
        var ptype=$("input[name='type']").val();
        var pnumber=$("input[name='number']").val();
        var pprice=$("input[name='price']").val();
        var pdateofproduce=$("input[name='dateofproduce']").val();
        var pdateofbad=$("input[name='dateofbad']").val();
        if(proID==''||proID=='undefined'||proID==null){
            alert("请输入商品ID");
        }
        else if(proName==''||proName==undefined||proName==null){
            alert("请输入商品名称");
        }
        else if(ptype==''||ptype==undefined||ptype==null){
            alert("请输入商品种类");
        }
        else if(pnumber==''||pnumber==undefined||pnumber==null){
            alert("请输入商品库存数量");
        }
        else if( pprice==''||pprice==undefined||pprice==null){
            alert("请输入商品单价");
        }
        else if(pdateofproduce==''||pdateofproduce==undefined||pdateofproduce==null){
            alert("请输入商品生产日期");
        }
        else if(pdateofbad==''||pdateofbad==undefined||pdateofbad==null){
            alert("请输入商品保质日期");
        }
        else{
            $('#frm').submit();
        }
    });
});

$(function() {
    $('#btnsearch').click(function () {
        var proID=$("input[name='proID']").val();
        if(proID==''||proID=='undefined'||proID==null){
            alert("请输入商品ID");
        }
        else {
            $('#frm').submit();
        }
    });
});
function pRead() {
    var x=document.getElementById('buttontype').value;
    document.getElementById('buttontype').value="pread";
    document.getElementById(x).submit();
}
function pUpdate() {
    var x=document.getElementById('buttontype').value;
    document.getElementById('buttontype').value="pupdate";
    document.getElementById(x).submit();
}