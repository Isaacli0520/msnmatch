function autocomplete(inp, user_name, take) {
    /*the autocomplete function takes two arguments,
    the text field id and username*/
  
    /*execute a function when someone writes in the text field:*/
    $(document).ready(function(){
      $(inp).on("input", function(e) {
        var auto_list ,auto_element ,i ,j ,val = this.value;
  
        /*close any already open lists of autocompleted values if input == None*/
        if (!val) { closeAllLists(); return false;}
  
        $.ajax({
          url: '/courses/ajax/course_search_result/',
          data: {
            'input': val,
          },
          dataType: 'json',
          success: function (data) {
            closeAllLists();
            /*create a DIV element that will contain the items (values):*/
            auto_list = document.createElement("DIV");
            auto_list.setAttribute("id", this.id + "autocomplete-list");
            auto_list.setAttribute("class", "autocomplete-items");
            auto_list.setAttribute("style","width:100%;")
            /*append the DIV element as a child of the autocomplete container:*/
            $(inp).parent().append(auto_list);
  
            if (data.retrieved_courses) {
              var re_cs = data.retrieved_courses;
              for (i = 0; i < re_cs.length; i++) {
                auto_element = document.createElement("DIV");
                auto_element.setAttribute("class", "autocomplete-item");
  
                var tables = document.createElement("table");
                var tablerow = document.createElement("tr");
                var table1 = document.createElement("td");
                var table2 = document.createElement("td");
                var add_del_span = document.createElement("span");
  
                auto_list.appendChild(auto_element);
                auto_element.appendChild(tables);
                tables.appendChild(tablerow);
                tablerow.appendChild(table1);
                tablerow.appendChild(table2);
                table2.appendChild(add_del_span);
  
                auto_element.setAttribute("value", re_cs[i]["course_number"]);
                tables.setAttribute("style","width:100%;");
                table1.setAttribute("class","autocomplete-cs");
                table1.setAttribute("style","width:80%;");
                table1.setAttribute("value", re_cs[i]["course_number"]);
                table2.setAttribute("style","width:7%;");
                if ((re_cs[i]["course_taking"] && take=="taking")||(re_cs[i]["course_taken"] && take=="taken")){
                  add_del_span.setAttribute("class","fas fa-trash-alt");
                  add_del_span.setAttribute("id",take);
                }
                else if((re_cs[i]["course_taking"] && take=="taken")||(re_cs[i]["course_taken"] && take=="taking")){
                  add_del_span.setAttribute("class","fas fa-ban");
                }
                else{
                  add_del_span.setAttribute("class","far fa-plus-square");
                  add_del_span.setAttribute("id",take);
                }
  
                add_del_span.setAttribute("value",re_cs[i]["course_number"]);
  
                var tmp_name =  re_cs[i]["course_number"] + " " + re_cs[i]["course_name"];
                for (j = 0; j < re_cs[i]["course_match"].length; j++){
                  if (re_cs[i]["course_match"][j] == 1){
                    table1.innerHTML += "<strong>" + tmp_name.substr(j, 1) + "</strong>";
                  }
                  else{
                    table1.innerHTML += tmp_name.substr(j, 1);
                  }
                }
              }
            }
          }
        });
      });
    });
  
    $(document).on("click","#taking", function(e) {
      e.stopImmediatePropagation();
      $.ajax({
        url: '/courses/ajax/course_taking_add_delete/',
        data: {
          'username': user_name,
          'course_number':$(e.target).attr("value"),
        },
        dataType: 'json',
        success: function (data) {
          if (data.exist) {
            $(e.target).attr("class", "fas fa-trash-alt");
          }
          else{
            $(e.target).attr("class", "far fa-plus-square");
          }
        }
      });
    });
  
    $(document).on("click","#taken", function(e) {
      e.stopImmediatePropagation();
      $.ajax({
        url: '/courses/ajax/course_taken_add_delete/',
        data: {
          'username': user_name,
          'course_number':$(e.target).attr("value"),
        },
        dataType: 'json',
        success: function (data) {
          if (data.exist) {
            $(e.target).attr("class", "fas fa-trash-alt");
          }
          else{
            $(e.target).attr("class", "far fa-plus-square");
          }
        }
      });
    });
    /*execute a function when someone clicks on the item value (DIV element):*/
    $(document).on("click", ".autocomplete-cs", function(e) {
          // $(inp).val($(e.target).attr("value"));
          // closeAllLists();
          window.location.href = "/courses/"+ $(e.target).attr("value");
        });
  
  
    /*make an item active when the mouse enters it and make it inactive when mouse leaves it*/
    /*$(".autocomplete-item").on({
          mouseenter : function(e){
          $(e.currentTarget).addClass("autocomplete-active");
          },
          mouseleave : function(e){
          $(e.currentTarget).removeClass("autocomplete-active");
          }
        });
        */
  
  
    function closeAllLists(element) {
      /*close all autocomplete lists in the document,
      except the one passed as an argument:*/
      var x = document.getElementsByClassName("autocomplete-items");
      for (var i = 0; i < x.length; i++) {
        if (element != x[i] && element != inp) {
          x[i].parentNode.removeChild(x[i]);
        }
      }
    }
    /*execute a function when someone clicks in the document:*/
    $(document).click(function(e){
      if ($(e.target).is("body")){
        closeAllLists(e.target);
      }
    });
  }
  