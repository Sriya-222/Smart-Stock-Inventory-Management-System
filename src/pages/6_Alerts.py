import streamlit as st

st.title("System Alerts")
st.write("Stay updated with system notifications and warnings.")

initial_alerts = [
    {
        "id": 1,
        "title": "Low Stock: Wireless Headphones",
        "description": "Only 5 units left in inventory. Reorder soon.",
        "severity": "high",
        "time": "2 hours ago",
        "read": False
    },
    {
        "id": 2,
        "title": "System Update Scheduled",
        "description": "Maintenance window tonight at 2:00 AM UTC.",
        "severity": "info",
        "time": "5 hours ago",
        "read": False
    },
    {
        "id": 3,
        "title": "Unusual Login Attempt",
        "description": "Blocked login from unauthorized IP address.",
        "severity": "medium",
        "time": "1 day ago",
        "read": False
    },
    {
        "id": 4,
        "title": "Monthly Target Reached",
        "description": "Congratulations! Sales target achieved for this month.",
        "severity": "success",
        "time": "2 days ago",
        "read": True
    }
]

if "alerts" not in st.session_state:
    st.session_state.alerts = initial_alerts

def mark_all_read():
    for a in st.session_state.alerts:
        a["read"] = True

def mark_read(alert_id):
    for a in st.session_state.alerts:
        if a["id"] == alert_id:
            a["read"] = True

def delete_alert(alert_id):
    st.session_state.alerts = [a for a in st.session_state.alerts if a["id"] != alert_id]

unread_count = sum(1 for a in st.session_state.alerts if not a["read"])

col1, col2 = st.columns([3, 1])
with col1:
    st.subheader(f"Alerts ({unread_count} Unread)")
with col2:
    if st.button("Mark all as read", disabled=unread_count==0):
        mark_all_read()
        st.rerun()

st.markdown("---")

if not st.session_state.alerts:
    st.info("All caught up! There are no new alerts to display.")
else:
    for alert in st.session_state.alerts:
        with st.container(border=True):
            c1, c2 = st.columns([5, 1])
            with c1:
                # Icon determining based on severity
                if alert["severity"] == "high":
                    st.error(f"**{alert['title']}**\n\n{alert['description']}\n\n*{alert['time']}*")
                elif alert["severity"] == "medium":
                    st.warning(f"**{alert['title']}**\n\n{alert['description']}\n\n*{alert['time']}*")
                elif alert["severity"] == "success":
                    st.success(f"**{alert['title']}**\n\n{alert['description']}\n\n*{alert['time']}*")
                else:
                    st.info(f"**{alert['title']}**\n\n{alert['description']}\n\n*{alert['time']}*")
            
            with c2:
                if not alert["read"]:
                    if st.button("Mark Read", key=f"read_{alert['id']}"):
                        mark_read(alert['id'])
                        st.rerun()
                if st.button("Dismiss", key=f"del_{alert['id']}"):
                    delete_alert(alert['id'])
                    st.rerun()
