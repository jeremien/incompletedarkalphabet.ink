<?php

use Slim\Factory\AppFactory;
use Slim\Views\Twig;
use Slim\Views\TwigMiddleware;

require __DIR__ . '/../vendor/autoload.php';

$app = AppFactory::create();

$twig = Twig::create(__DIR__ . '/../templates', ['cache' => false]);

$app->add(TwigMiddleware::create($app, $twig));

function get_list_of_directories($path) {

	$iter = new RecursiveIteratorIterator(
    new RecursiveDirectoryIterator($path, RecursiveDirectoryIterator::SKIP_DOTS),
    RecursiveIteratorIterator::SELF_FIRST,
    RecursiveIteratorIterator::CATCH_GET_CHILD // Ignore "Permission denied"
	);

	//add the $path to the array as we need to scan for files in $path
	$array_of_dirs[] = $path;

	//scan for folder and sub folders
	$paths = array($path);
	foreach ($iter as $path => $dir) {
		if ($dir->isDir()) {
			$array_of_dirs[] = $path;
		}
	}

	return $array_of_dirs;

}

$app->get('/', function ($request, $response) {

  $view = Twig::fromRequest($request);

  $dirPath = __DIR__ . '/../public/images';

  $array_of_directories = get_list_of_directories($dirPath);

  $final_array = array();

  foreach($array_of_directories as $key => $directory) {
    // ignore the root folder
    if ($key == 0) { continue; }

    $files = scandir($directory);



    foreach ($files as $file) {
      // ignore dot file
      if($file == ".") { continue; }
		  if($file == "..") { continue; }

      $output_array[] = array(
        'file_name' => $file,
      );
    }



    // array_push($final_array, basename($directory);

    // $final_array = array(
    //   basename($directory) => $output_array,
    // );

  }

  print_r($final_array);

  return $view->render($response, 'home.html', [
      'title' => 'home',
      // 'images' => $final_array['files']
   ]);
})->setName('home');

$app->run();
