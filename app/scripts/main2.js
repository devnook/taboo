
var TabooApp = angular.module('TabooApp', []);

TabooApp
  .config(['$routeProvider', function($routeProvider) {
    $routeProvider.
        when('/guess', {templateUrl: 'partials/task.html',   controller: GuessController}).
        when('/add', {templateUrl: 'partials/add.html', controller: AddController}).
        when('/describe', {templateUrl: 'partials/describe.html', controller: DescribeController}).
        otherwise({redirectTo: '/'});
  }])
  .config(
    function($interpolateProvider) {
      $interpolateProvider.startSymbol('{*');
      $interpolateProvider.endSymbol('*}');
  });

function GuessController($scope, $http, $timeout) {
  var sc = $scope;

  $http.get('/get_task').success(function(response) {
    sc.task = response['task'];
  });

  sc.guess = function() {
    console.log('ssssssss')
    var params = {
      'word': sc.guessedWord,
      'task_key': sc.task.key
    };
    console.log(params);
    $http.post('/guess', params).success(function(response) {
      sc.message = response['message'];
    });

  };

}

function AddController ($scope, $http) {
  var sc = $scope;

  sc.add = function() {
    var params = {
      'word': sc.word,
      'forbidden_words': sc.forbidden_words
    };
    $http.post('/add_word', params).success(function(response) {
      sc.message = response['message'];
      sc.word = '';
      sc.forbidden_words = '';
    });

  };
}


function TabooController($scope, $http, $timeout) {

  var sc = $scope;

  sc.availableWords;
  sc.currentWord;
  sc.counter = 0;


  $http.get('/get_words').success(function(response) {
    sc.availableWords = response;
  });

  sc.selectWord = function(wordObj, e) {
    sc.currentWord = wordObj;
    sc.currentDescriptionError = '';
    sc.currentDescription = '';
    sc.countDown(10);
  };

  sc.isSelectedWord = function(word) {
    return sc.currentWord === word;
  }

  sc.isCurrentWordSet = function() {
    return !!sc.currentWord;
  }

  sc.validateForbidden = function() {
    sc.currentDescription;
    for (var i = 0, word; word = sc.currentWord['forbidden_words'][i]; i++) {
      if (sc.currentDescription.indexOf(word) > -1) {
        sc.currentDescriptionError = 'Forbidden word! (' + word + ')';
      } else {
        sc.currentDescriptionError = '';
      }
    }
  }

  sc.countDown = function(countFrom) {
    sc.counter = countFrom;
    var countInterval = 100;

    var countDown_ = function() {
      sc.counter--;
      countDowntTimer = $timeout(countDown_, countInterval);
      if (sc.counter == 0) {
        $timeout.cancel(countDowntTimer);
      }
    }
    var countDowntTimer = $timeout(countDown_, countInterval);
  };

  sc.publish = function() {
    var params = {
      'word': sc.currentWord.word,
      'description': sc.currentDescription
    };
    console.log(params)
    $http.post('/publish', params).success(function(response) {
      sc.message = response['message'];
    });

  };


}