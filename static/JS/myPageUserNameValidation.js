function myPageUserNameValidation(){

    let name = document.getElementById('inputname').value;
    $('#nameValidationMsg').empty();

    if(name.length > 20){
        $('#nameValidationMsg').append("20자 이내로 적어주세요")
        return false
    }

    let i = 0;
    for(; i < name.length; i++){

        let temp = name[i].charCodeAt();

        if (temp >= 0 && temp <=64){
            break;
        }else if(temp >= 91 && temp <= 96){
            break;
        }else if(temp >= 123 && temp <= 127){
            break;
        }else{
            continue;
        }
    }

    if(i == name.length){
        return true;
    }

    $('#nameValidationMsg').append("한글과 영어만으로 이름을 지어 주세요")
    return false
}
//
// $('#inputname').focus(function (){
//     alert('ㄹㄹ');
//     console.log('선택');
// })
//
// $('#inputname').focus(console.log('선택2'));


function saveUserInfoInMyPage(){

    let nameValidation = myPageUserNameValidation(); //true or false
    let profileImgSrc = myPageProfileImgUpload();

    if(nameValidation == false ){
        return
    }

    let userName = document.getElementById('inputname').value;
    let userDesc = document.getElementById('inputintroduce').value;
    let userUniqueId = "2"
    if(typeof(profileImgSrc) == "boolean"){
        profileImgSrc = null;
    }

    $.ajax({
        type:"POST",
        url:"/saveUserInfoInMyPage",
        data:{
            userNameGive: userName,
            profileImgSrcGive: profileImgSrc,
            userDescGive: userDesc,
            userUniqueIdGive: userUniqueId
        },
        success: function(response){
            alert(response['msg']);
        }
    })

}

function myPageProfileImgUpload(){

    let file = new FormData();
    let resultSrc = '';

    let fileLength = document.getElementById('myPageProfileImgFileInput').files.length;
    // console.log(a);
    if (fileLength < 1){
        // $('#showNoneFileError').empty();
        // $('#showNoneFileError').append("파일을 선택해주세요");
        return false
    }

    let imgFile = document.getElementById('myPageProfileImgFileInput').files[0]
    // let c = "2"

    file.append("profileImg", imgFile);

    // console.log(file);

    $.ajax({
        url: '/uploadProfileImg',
        type: 'POST',
        dataType: 'json',
        data: file,
        cache: false,
        contentType: false,
        processData: false,
        success: function(response){

            // console.log(response['msg']);
            // console.log(response['profileImgSrc'])
            document.getElementById('myPageProfileImg').setAttribute("src", response['profileImgSrc'])

            // tempHtml = `
            //     <img src="${response['profileImgSrc']}" style="width:100px">
            // `
            //
            // $('#showImgDiv').empty();
            // $('#showImgDiv').append(tempHtml);
            resultSrc = response['profileImgSrc'];


        }
    })

    return resultSrc

}

