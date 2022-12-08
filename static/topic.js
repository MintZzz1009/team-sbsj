
      const topicList = ['🌕 전체', '📡 중개 플랫폼', '📷 라이프스타일', '💰 금융', '👫 소셜',
              '🎙 미디어', '✏️ 교육', '🚲 생산성', '🔗 블록체인', '💻 노코드', '🤖 인공지능',
              '🏘 커뮤니티', '📊 분석툴', '🎨 디자인'
      ]

      function showNewsfeedFilteredByTopic(topicNum){

        $.ajax({
          type:"POST",
          url:"/showNewsfeedFilteredByTopic",
          data: {topicNumGive : topicNum},
          success: function(response){

            document.getElementById("newsfeed__expansion").innerHTML = "";

            console.log(response['result']);
            let rows = response['result'];


            for (let i =0; i < rows.length; i++){

              if(rows[i]['user_profile_img_src'] == null){
                rows[i]['user_profile_img_src'] = '/static/img/nullProfileImg.png'
              }

              if (rows[i]['posting_text'].length > 55) {
              rows[i]['posting_text'] = rows[i]['posting_text'].substring(0, 55);
              rows[i]['posting_text'] += ".......";
              }

              let tempHTML = ``;
              for(let j=0; j < rows[i]['topics_array'].length; j++){
                tempHTML += `<div class="previewCard__topics__tag">${topicList[rows[i]['topics_array'][j]]}</div>`
              }

              $('#newsfeed__expansion').append(`
                                            <div class="newsfeed__newsfeed">
                                              <!-- Button trigger modal -->
                                              <div class="newsfeed__info">
                                                <a
                                                  href="#"
                                                  class="membersCards__list__eachCards newsfeed__writer"
                                                >
                                                  <div class="eachCards__inner-content-wrapper">
                                                  <img src ="${rows[i]['user_profile_img_src']}" class = "eachCards__avatar">
<!--                                                    <div class="eachCards__avatar"></div>-->
                                                    <div class="eachCards__info">
                                                      <div class="eachCards__info__id">${rows[i]['user_name']}</div>
                                                      <div class="eachCards__info__email">${rows[i]['user_email']}</div>
                                                    </div>
                                                  </div>
                                                </a>
                                              </div>
                                              <button
                                                type="button"
                                                class="newsfeed__previewCard btn btn-primary"
                                                data-bs-toggle="modal"
                                                data-bs-target="#exampleModal"
                                              >
                                                <div class="previewCard__image"></div>
                                                <div class="previewCard__contents">
                                                  <div class="previewCard__header">${rows[i]['posting_title']}</div>
                                                  <div class="previewCard__desc">
                                                    ${rows[i]['posting_text']}
                                                  </div>
                                                  <div class="previewCard__topics">
                                                    ${tempHTML}
                                                  </div>
                                                </div>
                                              </button>
                                            </div>
                                            <!-- Modal -->
                                            <div
                                              class="modal fade"
                                              id="exampleModal"
                                              tabindex="-1"
                                              aria-labelledby="exampleModalLabel"
                                              aria-hidden="true"
                                            >
                                              <div class="modal-dialog">
                                                <div class="modal-content">
                                                  <div class="modal-header">
                                                    <h1 class="modal-title fs-5" id="exampleModalLabel">
                                                      Modal title
                                                    </h1>
                                                    <button
                                                      type="button"
                                                      class="btn-close"
                                                      data-bs-dismiss="modal"
                                                      aria-label="Close"
                                                    ></button>
                                                  </div>
                                                  <div class="modal-body">...</div>
                                                  <div class="modal-footer">
                                                    <button
                                                      type="button"
                                                      class="btn btn-secondary"
                                                      data-bs-dismiss="modal"
                                                    >
                                                      Close
                                                    </button>
                                                    <button type="button" class="btn btn-primary">
                                                      Save changes
                                                    </button>
                                                  </div>
                                                </div>
                                              </div>
                                            </div>
              `)
            }
          }
        })
      }


      function showNewsfeedOnlyMine(userId){

        $.ajax({
            type:"POST",
            url:"/showNewsfeedOnlyMine",
            data: {userIdGive : userId},
            success: function(response){

                console.log(response['result']);

                let rows = response['result'];

                document.getElementById('newsfeed__expansion').innerHTML= '';

                for (let i = 0; i < rows.length; i++){
                    let tempHtml = ``;

                    for(let j = 0; j < rows[i]['topics_array'].length; j++){
                        tempHtml += `<div class="previewCard__topics__tag">${topicList[rows[i]['topics_array'][j]]}</div>`;
                    }

                    if (rows[i]['user_profile_img_src'] == null){
                        rows[i]['user_profile_img_src'] = '/static/img/nullProfileImg.png';
                    }

                    if(rows[i]['posting_text'].length > 55){
                        rows[i]['posting_text'] = rows[i]['posting_text'].substring(0, 55);
                        rows[i]['posting_text'] += ".......";
                    }

                    console.log(rows[i]['posting_text'].length);

                    $('#newsfeed__expansion').append(`<div class="newsfeed__newsfeed">
                                                      <!-- Button trigger modal -->
                                                      <div class="newsfeed__info">
                                                        <a
                                                          href="#"
                                                          class="membersCards__list__eachCards newsfeed__writer"
                                                        >
                                                          <div class="eachCards__inner-content-wrapper">
                                                            <img src="${rows[i]['user_profile_img_src']}" class="eachCards__avatar">
                                                            <div class="eachCards__info">
                                                              <div class="eachCards__info__id">${rows[i]['user_name']}</div>
                                                              <div class="eachCards__info__email">${rows[i]['user_email']}</div>
                                                            </div>
                                                          </div>
                                                        </a>
                                                      </div>
                                                      <button
                                                        type="button"
                                                        class="newsfeed__previewCard btn btn-primary"
                                                        data-bs-toggle="modal"
                                                        data-bs-target="#exampleModal"
                                                      >
                                                        <div class="previewCard__image"></div>
                                                        <div class="previewCard__contents">
                                                          <div class="previewCard__header">${rows[i]['posting_title']}</div>
                                                          <div class="previewCard__desc">
                                                            ${rows[i]['posting_text']}
                                                          </div>
                                                          <div class="previewCard__topics">
                                                                ${tempHtml}
                                                          </div>
                                                        </div>
                                                      </button>
                                                    </div>
                                                    <!-- Modal -->
                                                    <div
                                                      class="modal fade"
                                                      id="exampleModal"
                                                      tabindex="-1"
                                                      aria-labelledby="exampleModalLabel"
                                                      aria-hidden="true"
                                                    >
                                                      <div class="modal-dialog">
                                                        <div class="modal-content">
                                                          <div class="modal-header">
                                                            <h1 class="modal-title fs-5" id="exampleModalLabel">
                                                              Modal title
                                                            </h1>
                                                            <button
                                                              type="button"
                                                              class="btn-close"
                                                              data-bs-dismiss="modal"
                                                              aria-label="Close"
                                                            ></button>
                                                          </div>
                                                          <div class="modal-body">...</div>
                                                          <div class="modal-footer">
                                                            <button
                                                              type="button"
                                                              class="btn btn-secondary"
                                                              data-bs-dismiss="modal"
                                                            >
                                                              Close
                                                            </button>
                                                            <button type="button" class="btn btn-primary">
                                                              Save changes
                                                            </button>
                                                          </div>
                                                        </div>
                                                      </div>
                                                    </div>`)



                }

            }
        })
      }

      function showNewsfeedWithPostingId(postingId){

        $.ajax({
          type:"POST",
          url:"showNewsfeedWithPostingId",
          data:{postingIdGive : postingId},
          success: function(response){

          }
        })
      }
