<?php
require_once 'logger.php';
/**
 * assertEnvironment() make sure that we are operating safely
 *
 * Assert that we are on SSL and on appropriate level before continuing. If any
 * of the requirements are not met, we abort and close the connection.
 *
 * @param void
 * @return void
 */
function assertEnvironment()
{
	global $log_error_code;
	/*
	 * are we on SSL
	 */
	if (is_null($_SERVER['HTTPS'])) {
		Logger::log_event(LOG_NOTICE,
				  "[RI] ($log_error_code) Environment-variable 'HTTP' not available.");
		exit(0);
	}
	if (strtolower($_SERVER['HTTPS']) != 'on') {
		Logger::log_event(LOG_NOTICE,
				  "[RI] ($log_error_code) Server is not running on SSL. Blocking robot-connections.");
		exit(0);
	}
	/*
	 * SSLv3
	 */
	if (is_null($_SERVER['SSL_PROTOCOL'])) {
		Logger::log_event(LOG_NOTICE,
				  "[RI] ($log_error_code) Environment-variable 'SSL_PROTOCL' not available.");
		exit(0);
	}
	$protocol = strtolower($_SERVER['SSL_PROTOCOL']);
	if (!($protocol == 'sslv3' || $protocol == 'tlsv1')) {
		Logger::log_event(LOG_NOTICE,
				  "[RI] ($log_error_code) Not on proper ssl protocol. Need SSLv3/TLS. Got " .
				  $_SERVER['SSL_PROTOCOL']);
		exit(0);
	}

	/*
	 * do we have a client certificate?
	 */
	if (is_null($_SERVER['SSL_CLIENT_CERT'])) {
		Logger::log_event(LOG_NOTICE,
				  "[RI] ($log_error_code) Environment-variable 'SSL_CLIENT_CERT' not available.");
		exit(0);
	}
	$cert = $_SERVER['SSL_CLIENT_CERT'];
	if (!isset($cert) || $cert == "") {
		Logger::log_event(LOG_NOTICE, "[RI] ($log_error_code) Connection from client (".
				  $_SERVER['REMOTE_ADDR'].
				  ") without certificate. Dropping connection. Make sure apache is configured with SSLVerifyClient optional_no_ca");
		exit(0);
	}

	/*
	 * Is the certificate properly constructed (can Apache find the DN)?
	 */
	if (is_null($_SERVER['SSL_CLIENT_I_DN'])) {
		Logger::log_event(LOG_NOTICE, "Malformed certificate from " . $_SERVER['REMOTE_ADDR'] . ". Aborting.");
		exit(0);
	}

} /* end assertEnvironment() */
?>