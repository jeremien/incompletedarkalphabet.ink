<?php

use Slim\Factory\AppFactory;
use Slim\Views\Twig;
use Slim\Views\TwigMiddleware;

require __DIR__ . '/../vendor/autoload.php';

$app = AppFactory::create();

$twig = Twig::create(__DIR__ . '/../templates', ['cache' => false]);

$app->add(TwigMiddleware::create($app, $twig));

// function get_list_of_directories($path) {
//
// 	$iter = new RecursiveIteratorIterator(
//     new RecursiveDirectoryIterator($path, RecursiveDirectoryIterator::SKIP_DOTS),
//     RecursiveIteratorIterator::SELF_FIRST,
//     RecursiveIteratorIterator::CATCH_GET_CHILD // Ignore "Permission denied"
// 	);
//
// 	//add the $path to the array as we need to scan for files in $path
// 	$array_of_dirs[] = $path;
//
// 	//scan for folder and sub folders
// 	$paths = array($path);
// 	foreach ($iter as $path => $dir) {
// 		if ($dir->isDir()) {
// 			$array_of_dirs[] = $path;
// 		}
// 	}
//
// 	return $array_of_dirs;
//
// }

// function get_files_in_directory($directory) {
//
// 	$files = scandir($directory);
//
// 	// $output = array();
//
// 	// print_r($files);
//
// 	// foreach($file as $files) {
// 	// 	if($file == ".") { continue; }
// 	// 	if($file == "..") { continue; }
// 		// print_r($files);
// 		// array_push($output, $file);
// 	// }
//
// 	return $files;
//
// }

function pathToArray($path , $separator = '/') {
    if (($pos = strpos($path, $separator)) === false) {
        return array($path);
    }
    return array(substr($path, 0, $pos) => pathToArray(substr($path, $pos + 1)));
}

$app->get('/', function ($request, $response) {

  $view = Twig::fromRequest($request);

  // $dirPath = __DIR__ . '/../public/images/';
	$dirPath = 'images/';
	$results = array();

	if (is_dir($dirPath)) {
    $iterator = new RecursiveDirectoryIterator($dirPath);
    foreach ( new RecursiveIteratorIterator($iterator, RecursiveIteratorIterator::CHILD_FIRST) as $file ) {
        if ($file->isFile()) {
            $thispath = str_replace('\\', '/', $file);
            $thisfile = utf8_encode($file->getFilename());
            $results = array_merge_recursive($results, pathToArray($thispath));
        }
    }
	}

	// print_r($results);

  // $array_of_directories = get_list_of_directories($dirPath);
	//
  // $final_array = array();
	//
  // foreach($array_of_directories as $key => $directory) {
  //   // ignore the root folder
  //   if ($key == 0) { continue; }
	//
	// 	// print_r($directory);
	//
	// 	// $files = get_files_in_directory($directory);
	// 	$files = scandir($directory);
	//
	// 	// print_r($files[2]);
	//
  //   // $files = scandir($directory);
	// 	//
  //   foreach ($files as $file) {
  //     // ignore dot file
  //     if($file == ".") { continue; }
	// 	  if($file == "..") { continue; }
	//
  //     $output_array[] = array(
  //       'file_name' => $file,
  //     );
	//
  //   }
	//
	// 	$files_array = array(
  //     basename($directory) => $output_array,
  //   );
	//
	// 	// print_r($output_array);
	//
  //   // array_push($final_array, basename($directory);
	//
  //   array_push($final_array, $files_array);
	//
  // }
	//
  // print_r($final_array['arbres']);

  return $view->render($response, 'home.html', [
      'title' => 'home',
      'images' => $results['images']
   ]);
})->setName('home');

$app->run();
