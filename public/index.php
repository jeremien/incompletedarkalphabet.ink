<?php

use Slim\Factory\AppFactory;
use Slim\Views\Twig;
use Slim\Views\TwigMiddleware;

require __DIR__ . '/../vendor/autoload.php';

$app = AppFactory::create();

$twig = Twig::create(__DIR__ . '/../templates', ['cache' => false]);

$app->add(TwigMiddleware::create($app, $twig));

/* fonction recusive pour écrire le nom des dossiers et des fichiers */
function pathToArray($path , $separator = '/') {
    if (($pos = strpos($path, $separator)) === false) {
        return array($path);
    }
    return array(substr($path, 0, $pos) => pathToArray(substr($path, $pos + 1)));
}


$app->get('/', function ($request, $response) {

  $view = Twig::fromRequest($request);

	$dirPath = 'images/';
	$results = array();

  /* fonction pour parcourir le système de fichier
  et fabriquer un tableau à plusieurs dimensions
  avec le nom des dossiers et fichiers */
	if (is_dir($dirPath)) {
    $iterator = new RecursiveDirectoryIterator($dirPath);
    foreach ( new RecursiveIteratorIterator($iterator, RecursiveIteratorIterator::CHILD_FIRST) as $file ) {
        if ($file->isFile()) {
            $thispath = str_replace('\\', '/', $file);
            $results = array_merge_recursive($results, pathToArray($thispath));
        }
    }
	}

  // foreach ($results as $result) {
  //   print_r($result);
  //   foreach ($result as $image) {
  //     print_r($image);
  //   }
  // }

  return $view->render($response, 'home.html', [
      'title' => 'home',
      'images' => $results['images']
   ]);
})->setName('home');

$app->run();
