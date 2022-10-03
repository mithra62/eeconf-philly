<?php

return [
    'author' => 'Me',
    'author_url' => 'https://me.com',
    'docs_url' => 'https://www.me.com/docs/',
    'name' => 'Example Command Line Route',
    'description' => 'Adds a Command Line that can work as a Service',
    'version' => '1.0.0',
    'namespace' => 'Your\Namespace',
    'settings_exist' => false,
    'commands' => [
        'twitter:account:sync' => Your\Namespace\Commands\Twitter\Account\Sync::class,
    ],
];
