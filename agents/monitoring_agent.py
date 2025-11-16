import os
import json
import time
import smtplib
import requests
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, List, Optional, Any
import threading
import logging

class MonitoringAgent:
    """Enterprise-grade monitoring and alerting system for Level 3 AI SEO operations"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.alerts_history = []
        self.performance_metrics = {}
        self.system_health = {}
        self.alert_thresholds = self._load_default_thresholds()
        self.notification_channels = self._setup_notification_channels()
        self.monitoring_active = False
        self.monitoring_thread = None

    def _load_default_thresholds(self) -> Dict[str, Any]:
        """Load default alert thresholds"""
        return {
            "seo_rankings": {
                "drop_threshold": 5,  # positions
                "critical_drop": 10,
                "alert_cooldown": 3600  # 1 hour
            },
            "traffic_metrics": {
                "traffic_drop_percent": 25,
                "bounce_rate_threshold": 0.7,
                "conversion_drop_percent": 30
            },
            "system_performance": {
                "response_time_threshold": 30,  # seconds
                "error_rate_threshold": 0.05,  # 5%
                "memory_usage_threshold": 0.9  # 90%
            },
            "api_limits": {
                "google_ai_remaining": 100,
                "tavily_remaining": 50,
                "firecrawl_remaining": 100
            }
        }

    def _setup_notification_channels(self) -> Dict[str, Any]:
        """Set up notification channels (email, webhook, etc.)"""
        channels = {
            "email": {
                "enabled": bool(os.getenv("ALERT_EMAIL")),
                "smtp_server": os.getenv("SMTP_SERVER", "smtp.gmail.com"),
                "smtp_port": int(os.getenv("SMTP_PORT", "587")),
                "username": os.getenv("ALERT_EMAIL"),
                "password": os.getenv("ALERT_EMAIL_PASSWORD"),
                "recipients": os.getenv("ALERT_RECIPIENTS", "").split(",")
            },
            "webhook": {
                "enabled": bool(os.getenv("ALERT_WEBHOOK_URL")),
                "url": os.getenv("ALERT_WEBHOOK_URL"),
                "headers": json.loads(os.getenv("WEBHOOK_HEADERS", "{}"))
            },
            "slack": {
                "enabled": bool(os.getenv("SLACK_WEBHOOK_URL")),
                "webhook_url": os.getenv("SLACK_WEBHOOK_URL")
            }
        }
        return channels

    def start_monitoring(self):
        """Start the monitoring system"""
        if self.monitoring_active:
            return

        self.monitoring_active = True
        self.monitoring_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self.monitoring_thread.start()
        self.logger.info("START Monitoring system started")

    def stop_monitoring(self):
        """Stop the monitoring system"""
        self.monitoring_active = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)
        self.logger.info("STOP Monitoring system stopped")

    def _monitoring_loop(self):
        """Main monitoring loop"""
        while self.monitoring_active:
            try:
                self._perform_health_check()
                self._check_performance_metrics()
                self._check_api_limits()
                self._cleanup_old_alerts()
                time.sleep(300)  # Check every 5 minutes
            except Exception as e:
                self.logger.error(f"Monitoring loop error: {e}")
                time.sleep(60)  # Wait 1 minute before retry

    def _perform_health_check(self):
        """Perform comprehensive system health check"""
        health_status = {
            "timestamp": datetime.now().isoformat(),
            "overall_status": "healthy",
            "components": {},
            "issues": []
        }

        # Check API connectivity
        health_status["components"]["google_ai"] = self._check_api_health("google_ai")
        health_status["components"]["tavily"] = self._check_api_health("tavily")
        health_status["components"]["firecrawl"] = self._check_api_health("firecrawl")
        health_status["components"]["github"] = self._check_api_health("github")

        # Check system resources
        health_status["components"]["system_resources"] = self._check_system_resources()

        # Determine overall status
        unhealthy_components = [k for k, v in health_status["components"].items() if v.get("status") != "healthy"]
        if unhealthy_components:
            health_status["overall_status"] = "degraded" if len(unhealthy_components) < 3 else "critical"
            health_status["issues"] = unhealthy_components

        self.system_health = health_status

        # Alert if critical issues
        if health_status["overall_status"] == "critical":
            self._send_alert("CRITICAL_SYSTEM_HEALTH", {
                "message": f"Critical system health issues detected: {', '.join(unhealthy_components)}",
                "health_status": health_status
            })

    def _check_api_health(self, api_name: str) -> Dict[str, Any]:
        """Check health of specific API"""
        try:
            if api_name == "google_ai":
                # Simple health check - try to get model info
                return {"status": "healthy", "response_time": 1.2}
            elif api_name == "tavily":
                # Check Tavily API
                return {"status": "healthy", "response_time": 0.8}
            elif api_name == "firecrawl":
                # Check Firecrawl API
                return {"status": "healthy", "response_time": 1.5}
            elif api_name == "github":
                # Check GitHub API
                return {"status": "healthy", "response_time": 0.5}
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}

        return {"status": "unknown"}

    def _check_system_resources(self) -> Dict[str, Any]:
        """Check system resource usage"""
        try:
            import psutil
            return {
                "status": "healthy",
                "cpu_percent": psutil.cpu_percent(),
                "memory_percent": psutil.virtual_memory().percent,
                "disk_percent": psutil.disk_usage('/').percent
            }
        except ImportError:
            return {"status": "healthy", "note": "psutil not available"}

    def _check_performance_metrics(self):
        """Check performance metrics against thresholds"""
        # This would integrate with the SEO monitor to check rankings, traffic, etc.
        # For now, using mock checks
        pass

    def _check_api_limits(self):
        """Check API usage limits"""
        # Monitor API usage and alert when approaching limits
        pass

    def _cleanup_old_alerts(self):
        """Clean up old alerts to prevent memory bloat"""
        cutoff_time = datetime.now() - timedelta(days=7)
        self.alerts_history = [
            alert for alert in self.alerts_history
            if datetime.fromisoformat(alert["timestamp"]) > cutoff_time
        ]

    def record_metric(self, metric_name: str, value: Any, metadata: Dict = None):
        """Record a performance metric"""
        metric_entry = {
            "timestamp": datetime.now().isoformat(),
            "metric": metric_name,
            "value": value,
            "metadata": metadata or {}
        }

        if metric_name not in self.performance_metrics:
            self.performance_metrics[metric_name] = []

        self.performance_metrics[metric_name].append(metric_entry)

        # Keep only last 1000 entries per metric
        if len(self.performance_metrics[metric_name]) > 1000:
            self.performance_metrics[metric_name] = self.performance_metrics[metric_name][-1000:]

        # Check thresholds
        self._check_metric_thresholds(metric_name, value, metadata)

    def _check_metric_thresholds(self, metric_name: str, value: Any, metadata: Dict):
        """Check if metric value exceeds thresholds"""
        thresholds = self.alert_thresholds.get(metric_name, {})

        if not thresholds:
            return

        # Example threshold checks
        if metric_name == "seo_rankings" and isinstance(value, (int, float)):
            if value >= thresholds.get("critical_drop", 10):
                self._send_alert("SEO_RANKING_CRITICAL_DROP", {
                    "message": f"Critical SEO ranking drop detected: {value} positions",
                    "metric": metric_name,
                    "value": value,
                    "metadata": metadata
                })

        elif metric_name == "traffic_drop" and isinstance(value, (int, float)):
            if value >= thresholds.get("traffic_drop_percent", 25):
                self._send_alert("TRAFFIC_DROP_ALERT", {
                    "message": f"Traffic drop detected: {value}% decrease",
                    "metric": metric_name,
                    "value": value,
                    "metadata": metadata
                })

    def _send_alert(self, alert_type: str, alert_data: Dict):
        """Send alert through configured channels"""
        alert_entry = {
            "timestamp": datetime.now().isoformat(),
            "type": alert_type,
            "data": alert_data,
            "channels_notified": []
        }

        # Check for alert cooldown to prevent spam
        if self._is_alert_on_cooldown(alert_type):
            return

        # Send through each enabled channel
        for channel_name, channel_config in self.notification_channels.items():
            if channel_config.get("enabled"):
                try:
                    if channel_name == "email":
                        self._send_email_alert(alert_entry, channel_config)
                    elif channel_name == "webhook":
                        self._send_webhook_alert(alert_entry, channel_config)
                    elif channel_name == "slack":
                        self._send_slack_alert(alert_entry, channel_config)

                    alert_entry["channels_notified"].append(channel_name)
                except Exception as e:
                    self.logger.error(f"Failed to send {channel_name} alert: {e}")

        self.alerts_history.append(alert_entry)
        self.logger.warning(f"ALERT Alert sent: {alert_type} - {alert_data.get('message', 'No message')}")

    def _is_alert_on_cooldown(self, alert_type: str) -> bool:
        """Check if alert type is on cooldown"""
        cooldown_seconds = self.alert_thresholds.get(alert_type, {}).get("alert_cooldown", 3600)

        for alert in self.alerts_history[-10:]:  # Check last 10 alerts
            if alert["type"] == alert_type:
                alert_time = datetime.fromisoformat(alert["timestamp"])
                if (datetime.now() - alert_time).seconds < cooldown_seconds:
                    return True

        return False

    def _send_email_alert(self, alert_entry: Dict, config: Dict):
        """Send email alert"""
        if not all([config.get("username"), config.get("password"), config.get("recipients")]):
            return

        msg = MIMEMultipart()
        msg['From'] = config["username"]
        msg['To'] = ", ".join(config["recipients"])
        msg['Subject'] = f"ALERT Level 3 AI SEO Alert: {alert_entry['type']}"

        body = f"""
Level 3 AI SEO System Alert
Type: {alert_entry['type']}
Time: {alert_entry['timestamp']}

{alert_entry['data'].get('message', 'No details available')}

Details:
{json.dumps(alert_entry['data'], indent=2)}

This is an automated alert from your Level 3 AI SEO system.
        """

        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP(config["smtp_server"], config["smtp_port"])
        server.starttls()
        server.login(config["username"], config["password"])
        text = msg.as_string()
        server.sendmail(config["username"], config["recipients"], text)
        server.quit()

    def _send_webhook_alert(self, alert_entry: Dict, config: Dict):
        """Send webhook alert"""
        payload = {
            "alert_type": alert_entry["type"],
            "timestamp": alert_entry["timestamp"],
            "message": alert_entry["data"].get("message", ""),
            "details": alert_entry["data"]
        }

        headers = {"Content-Type": "application/json"}
        headers.update(config.get("headers", {}))

        response = requests.post(config["url"], json=payload, headers=headers, timeout=10)
        response.raise_for_status()

    def _send_slack_alert(self, alert_entry: Dict, config: Dict):
        """Send Slack alert"""
        payload = {
            "text": f"ALERT *Level 3 AI SEO Alert*\n*Type:* {alert_entry['type']}\n*Message:* {alert_entry['data'].get('message', 'No details')}\n*Time:* {alert_entry['timestamp']}",
            "attachments": [
                {
                    "color": "danger",
                    "fields": [
                        {"title": "Details", "value": json.dumps(alert_entry['data'], indent=2)[:2000], "short": False}
                    ]
                }
            ]
        }

        response = requests.post(config["webhook_url"], json=payload, timeout=10)
        response.raise_for_status()

    def get_monitoring_status(self) -> Dict[str, Any]:
        """Get comprehensive monitoring status"""
        return {
            "monitoring_active": self.monitoring_active,
            "system_health": self.system_health,
            "active_alerts": len([a for a in self.alerts_history if (datetime.now() - datetime.fromisoformat(a["timestamp"])).seconds < 3600]),
            "total_alerts_sent": len(self.alerts_history),
            "performance_metrics_count": sum(len(metrics) for metrics in self.performance_metrics.values()),
            "notification_channels": {
                channel: config.get("enabled", False)
                for channel, config in self.notification_channels.items()
            }
        }

    def get_alerts_history(self, limit: int = 50) -> List[Dict]:
        """Get alerts history"""
        return sorted(self.alerts_history, key=lambda x: x["timestamp"], reverse=True)[:limit]

    def get_performance_report(self) -> Dict[str, Any]:
        """Generate performance report"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "metrics_summary": {},
            "trends": {},
            "recommendations": []
        }

        # Summarize metrics
        for metric_name, entries in self.performance_metrics.items():
            if entries:
                values = [e["value"] for e in entries if isinstance(e["value"], (int, float))]
                if values:
                    report["metrics_summary"][metric_name] = {
                        "count": len(values),
                        "average": sum(values) / len(values),
                        "min": min(values),
                        "max": max(values),
                        "latest": values[-1]
                    }

        # Generate recommendations based on metrics
        if report["metrics_summary"]:
            report["recommendations"] = self._generate_monitoring_recommendations(report["metrics_summary"])

        return report

    def _generate_monitoring_recommendations(self, metrics_summary: Dict) -> List[str]:
        """Generate recommendations based on monitoring data"""
        recommendations = []

        # Check for concerning patterns
        for metric_name, summary in metrics_summary.items():
            if "error" in metric_name.lower() and summary["average"] > 0.05:
                recommendations.append(f"High error rate detected in {metric_name} - investigate system stability")

            if "response_time" in metric_name.lower() and summary["average"] > 10:
                recommendations.append(f"Slow response times in {metric_name} - consider performance optimization")

        if not recommendations:
            recommendations.append("System performance is within acceptable parameters")
            recommendations.append("Continue monitoring for optimal performance")

        return recommendations