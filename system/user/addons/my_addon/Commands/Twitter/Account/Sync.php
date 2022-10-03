<?php

namespace Your\Namespace\Commands\Twitter\Account;

use ExpressionEngine\Cli\Cli;

class Sync extends Cli
{
    /**
     * name of command
     * @var string
     */
    public $name = 'Twitter Account Sync';

    /**
     * signature of command
     * @var string
     */
    public $signature = 'twitter:account:sync';

    /**
     * Public description of command
     * @var string
     */
    public $description = 'Syncs a twitter account with us using a queue approach';

    /**
     * Summary of command functionality
     * @var [type]
     */
    public $summary = 'Syncs a twitter account with us';

    /**
     * How to use command
     * @var string
     */
    public $usage = 'php eecli.php twitter:account:sync';

    /**
     * options available for use in command
     * @var array
     */
    public $commandOptions = [
        'service,s' => 'Run this command as a Service rather than via Cron or Terminal.',
    ];

    /**
     * Run the command
     * @return mixed
     */
    public function handle()
    {
        $controller = new \Controller();
        if ($this->option('-s', false)) {
            $this->handleAsService();
        } else {
            ee('my_addon:Twitter')->sync();
        }
    }

    /**
     * Run the command as a service
     * @return mixed
     */
    private function handleAsService()
    {
        while (true) {
            ee('my_addon:Twitter')->sync();
        }
    }
}
