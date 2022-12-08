$(document).ready(function () {
    show_all_posting();
});

// 뉴스피드 조회
function show_all_posting() {
    console.log('show_all_posting 작동 시작')
    $.ajax({
        type: "GET",
        url: "main",
        data: {},
        success: function (response) {
            console.log('show_all_posting 응답 성공')
            let rows = response['posting__box']
            console.log(response['posting__box'])

            for (let i = 0; i < rows.length; i++) {
                let user_unique_id = rows[i][0]
                let posting_id = rows[i][1]
                let posting_text = rows[i][2]
                let posting_topic = rows[i][3]
                let posting_title = rows[i][4]
                let user_id = rows[i][8]

                let user_name = rows[i][11]
                let user_email = rows[i][12]
                let user_desc = rows[i][14]
                let user_profile_img_src = rows[i][15]
                let showpostbox =
                    new PostingBox(
                        user_unique_id,
                        posting_id,
                        posting_text,
                        posting_topic,
                        posting_title,
                        user_id,
                        user_name,
                        user_email,
                        user_desc)
                showpostbox.ShowPostBox()
            }
        }
    })

    class PostingBox {
        constructor(user_unique_id,
                    posting_id,
                    posting_text,
                    posting_topic,
                    posting_title,
                    user_id,
                    user_name,
                    user_email,
                    user_desc) {
            this.user_unique_id = user_unique_id
            this.posting_id = posting_id
            this.posting_text = posting_text
            this.posting_topic = posting_topic
            this.posting_title = posting_title
            this.user_id = user_id
            this.user_name = user_name
            this.user_email = user_email
            this.user_desc = user_desc

        }

        ShowPostBox() {
            let temp_html = `
                <div class="newsfeed__newsfeed">
                    <div class="newsfeed__info">
                        <a href="#" class="membersCards__list__eachCards newsfeed__writer">
                            <div class="eachCards__inner-content-wrapper">
                                <div class="eachCards__avatar"></div>
                                <div class="eachCards__info">
                                    <div class="eachCards__info__id">${this.user_id}</div>
                                    <div class="eachCards__info__email">${this.user_email}</div>
                                </div>
                            </div>
                        </a>
                    </div>
                    <button id="${this.posting_id}" onclick="OpenPostBox(${this.post_num}, ${this.posting_id}, '${this.user_id}','${this.user_email}','${this.posting_title}','${this.user_desc}','${this.topic_num_0}','${this.topic_num_1}','${this.topic_num_2}')" class="newsfeed__previewCard">
                        <div class="previewCard__image"></div>
                        <div class="previewCard__contents">
                            <div class="previewCard__header">${this.posting_title}</div>
                            <div class="previewCard__desc">
                                ${this.user_desc}
                            </div>
                            <div class="previewCard__topics">
                                <div class="previewCard__topics__tag">${this.topic_num_0}</div>
                                <div class="previewCard__topics__tag">${this.topic_num_1}</div>
                                <div class="previewCard__topics__tag">${this.topic_num_2}</div>
                            </div>
                        </div>
                    </button>
                </div>
            </div>`
            $('#newsfeed__expansion').append(temp_html)
        }
    }
}

function OpenPostBox(user_unique_id,
                     posting_id,
                     posting_text,
                     posting_topic,
                     posting_title,
                     user_id,
                     user_name,
                     user_email,
                     user_desc) {
    console.log(user_unique_id,
        posting_id,
        posting_text,
        posting_topic,
        posting_title,
        user_id,
        user_name,
        user_email,
        user_desc)
    let pt = posting_text
    let ud = user_desc
    let pid = posting_id
    $.ajax({
        type: "GET",
        url: "/show_comment",
        data: {},
        success: function (response) {
            let rows = response["msg"]
            console.log(rows)
            for ( let i = 0; i < rows.length; i++) {
                let comment_id = rows[i]['comment_id']
                let comment = rows[i]['comment']
                let clock = rows[i]['clock']

                let temp_html = `
                                <div class="comment-contain">
                                    <div class="comment-name">
                                        이름
                                    </div>
                                    <div class="comment_comment">
                                        <div class="body-comment">
                                        
                                            <span id=span_${comment_id}>${comment}</span>
                                        
                                        </div>
                                    </div>
                                    <div class="comment-button">
                                        <button onclick="addInput(${comment_id})" type="button" class="btn btn-warning button1">수정</button>
                                    </div>
                                </div>
                                <div class="clock">
                                        ${clock}
                                </div>
                                    `
                $(".modal-comment-body").append(temp_html)
            }
            
        }
    })

    let temp_html = `<div class="read-modal read-hidden">
                                <div class="read-modal-overlay" onclick="OffModal()"></div>
                                <div class="read-modal-content">
                                    <div class="read-modal-posting-title">
                                        <div class="read-modal-user-img">
                                            <img src="../static/image/sbsj_signature.PNG" class="read-modal-user-img-img">
                                        </div>
                                        <div>${pt}</div>
                                        <div class="read-modal-sbsj-img">
                                            <button id="read-exit-posting" onclick="OffModal()"><img style="float: right;height: 70px; width:70px"
                                                                                src="static/image/sbsj_signature.png"
                                                                                class="read-modal-user-img-img">
                                            </button>
                                        </div>
                                    </div>
                                    <div class="read-modal-posting-contents">
                                        ${ud}
                                    </div>
                                    <div class="read-modal-comment-form">
                                        <div class="modal-comment-container">
                                            <div class="modal-comment-title">
                                                댓글
                                            </div>
                                            <div id="${pid}" class="modal-comment-body">
                                                
                                            </div>
                                            <div class="modal-comment-bottom">
                                                <div class="modal-input-text">
                                                    <input id="comment" type="text" class="comment-input-contents"
                                                           placeholder="내용을 입력해주세요"><br><br>
                                                </div>
                                                <div class="modal-input-button">
                                                    <button onclick="save_comment()" class="btn btn-warning btn-lg comment1">등록</button>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>`
    $('#newsfeed__expansion').append(temp_html);
    document.querySelector(".read-modal").classList.remove("read-hidden");
}

function comments_get() {
    //댓글 조회 만들기
}

// 모달창 끄기
function OffModal() {
    $(".read-modal").remove();
}

// 게시글 작성시 topic 개수 선택 설정하기
function topic_value_get() {
    const topic_values = [];
    var topic = $("input[name='topic']:checked");

    for (let i = 0; i < topic.length; i++) {
        console.log(topic[i])
        topic_values.push(topic[i].value);
        if (topic_values.length > 3) {
            alert("토픽은 3개까지 설정 가능합니다.");
            return;
        }
    }
    let topic_value_join_string = topic_values.join(" ");

    return topic_value_join_string;
}

// 게시글 생성
function new_posting() {
    console.log('new posting 함수 시작')
    let title = $("#posting_title").val();
    let text = $("#posting_text").val();
    let topic = topic_value_get();
    let user = 5;
    $.ajax({
        type: "POST",
        url: "/mypage/newsfeed",
        data: {
            user_id_give: user,
            posting_title_give: title,
            posting_text_give: text,
            posting_topic_give: topic,
        },
        success: function (response) {
            alert(response["msg"]);
            window.location.reload();
        },
    });
}

// 댓글 저장
function save_comment() {
    console.log('댓글 저장 시작')
    let comment = $("#comment").val();
    let clock = Date.now();
    console.log(comment)

    $.ajax({
        type: "POST",
        url: "/save_comment",
        data: {comment_give: comment, clock_give: clock},
        success: function (response) {
            console.log(response)
            alert(response["msg"]);
            $(".modal-comment-body").empty()
            OpenPostBox()
        },
    });
}

// 댓글 수정
function addInput(comment_id) {
    console.log(comment_id)
    let a = $(`#span_${comment_id}`)
    let addinput = $(`#span_${comment_id}`).text()
    console.log(a)
    console.log(addinput)
    a.empty()
    a.append($("<input>", {id:"abcd", type: "text", value: addinput}))
    a.append($(`<button id="edit-${comment_id}" >수정완료!</button>`))

    $(`#edit-${comment_id}`).click(function () {
        update_comment(comment_id)
        
        console.log('수정완료! 버튼 실행 완료')
    })
}

// 댓글 수정 완료
function update_comment(comment_id) {
    console.log(comment_id)

    let edit_comment_id = $(`#span_${comment_id} input`).val()

        console.log(edit_comment_id)
        console.log($(`#span_${comment_id} input`))

    $.ajax({
        type: "POST",
        url: "/update/comment",
        data: {edit_done_give: comment_id, edit_comment_id_give: edit_comment_id},
        success: function (response) {
            alert(response["msg"])
            $(".modal-comment-body").empty()
            OpenPostBox()
        }
    })
}

// 몇분 전 시간 표시
function time_stemp(dt) {

    const today_time = Date.now();
    const past_time = dt;
    let set_time = today_time - past_time


    if (set_time < 60000) {
        return `${parseInt(set_time / 1000)}초 전`
    } else if (set_time < 3600000) {
        return `${parseInt(set_time / 1000 / 60)}분 전`
    } else if (set_time < 86400000) {
        return `${parseInt(set_time / 1000 / 60 / 60)}시간 전`
    } else {
        return `${parseInt(set_time / 1000 / 60 / 60 / 24)}일 전`
    }
}

