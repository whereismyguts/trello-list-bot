Vue.component('blog-post', {
  props: ['title'],
  template: '<h3>{{! title }}</h3>'
});


var App = new Vue({
  el: "#app",
  data: function () {
    return {
      wait: true,
      cards:[],
      username:'',
      new_card: {
        title: '',
        desc: '',
        adding: false
      }
    }
  },
  created: function () {
    // Alias the component instance as `vm`, so that we  
    // can access it inside the promise function
    
    // Fetch our array of posts from an API

    url = 'api/hello';
    // fetch('api/hello')
    //   .then(function (response) {
    //     return response.json()
    //   })
    //   .then(function (data) {
    //     vm.cards = data.cards;
    //     vm.username = data.username;
    //   })

    data = {test: 3};
    this.post_request(url, data)
  },
  mounted() {
    var self = this;
    /*
    $.getJSON(
      "https://api.jsonbin.io/b/5bf56501746e9b593ec0e909/3",
      function(data) {
        self.doc = {
          true: data.en,
          false: data.ru
        };
        self.toggleLocale();
      }
    );
    */
  },
  methods: {
    change_card: function(card) {
      card.is_edit = false;
      this.post_request(
        'api/change_card', 
        {
          id: card.id,
          title: card.title,
          desc: card.desc,
        }
      )
    },
    remove_item: function(link) {
      if (confirm("Are you confirm deleting this item?") == false)
        return;
      
      this.post_request(
        'api/remove_item', 
        {
          id: link.id,
        }
      )
    },
    add_link: function(card) {
      card.links.push(
        {
          url: card.new_link_url,
          text: card.new_link_text 
        }
      );
      card.link_adding = false;
      if (!this.post_request(
        'api/add_link', 
        {
          id: card.id,
          url: card.new_link_url,
          text: card.new_link_text
        }
      )){
        alert('Something wrong');
        card.links.pop()
      }

    },
    add_card: function(card) {
      
      this.post_request(
        'api/add_card', 
        {
          title: card.title,
          desc: card.desc
        }
      )
    },
    post_request: function(url, data) {
      var vm = this;
      fetch(url, {
        method: "POST", // *GET, POST, PUT, DELETE, etc.
        //mode: "cors", // no-cors, cors, *same-origin
        //cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
        //credentials: "same-origin", // include, *same-origin, omit
        headers: {
            "Content-Type": "application/json",
            // "Content-Type": "application/x-www-form-urlencoded",
        },
        //redirect: "follow", // manual, *follow, error
        //referrer: "no-referrer", // no-referrer, *client
        body: JSON.stringify(data), // body data type must match "Content-Type" header
      })
      .then(function (response) {
        return response.json()
      })
      .then(function (data) {
        vm.cards = data.cards;
        vm.username = data.username;
        vm.wait = false;
        
      })
      return true
    }
  }
});

