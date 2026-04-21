"""Discord Embed Formatters for Time Tracker"""
import discord
from typing import Dict, Any, List
from datetime import datetime


class EmbedFormatter:
    """Format Discord embeds for time tracking responses"""
    
    COLOR_SUCCESS = discord.Color.green()
    COLOR_ERROR = discord.Color.red()
    COLOR_INFO = discord.Color.blue()
    COLOR_WARNING = discord.Color.orange()
    
    def help_embed(self, is_admin: bool = False) -> discord.Embed:
        """!clock help - Show command help"""
        embed = discord.Embed(
            title="⏰ Time Tracker Commands",
            description="Track your work time and view pay",
            color=self.COLOR_INFO
        )
        
        # User commands
        user_cmds = (
            "`!clock in` - Start your work session (requires desktop agent)\n"
            "`!clock out` - End your work session\n"
            "`!clock pay` - View your unpaid time and earnings\n"
            "`!clock help` - Show this help message"
        )
        embed.add_field(
            name="👤 User Commands",
            value=user_cmds,
            inline=False
        )
        
        # Admin commands
        if is_admin:
            admin_cmds = (
                "`!clock hourlyrate @user 15` - Set hourly rate\n"
                "`!clock addtime 30 @user` - Add minutes to user\n"
                "`!clock removetime 30 @user` - Remove minutes from user\n"
                "`!clock day @user` - Today's summary\n"
                "`!clock week @user` - Last 7 days summary\n"
                "`!clock who` - Currently clocked in users\n"
                "`!clock status @user` - User status\n"
                "`!clock clear` - Mark all as paid"
            )
            embed.add_field(
                name="⚙️ Admin Commands",
                value=admin_cmds,
                inline=False
            )
        
        embed.set_footer(
            text="Timezone: America/New_York | Sessions rounded to nearest minute"
        )
        return embed
    
    def pay_summary_embed(self, user: discord.User, data: Dict[str, Any]) -> discord.Embed:
        """Format pay summary for !clock pay"""
        hours = data.get('hours_worked', 0)
        minutes = data.get('minutes_worked', 0)
        rate = data.get('hourly_rate', 0)
        amount = data.get('pay_amount', 0)
        
        embed = discord.Embed(
            title=f"💰 Pay Summary for {user.display_name}",
            color=self.COLOR_SUCCESS
        )
        
        embed.add_field(name="Total Time", value=f"{hours}h {minutes}m", inline=True)
        embed.add_field(name="Hourly Rate", value=f"${rate:.2f}", inline=True)
        embed.add_field(name="Amount Owed", value=f"${amount:.2f}", inline=True)
        
        if data.get('session_minutes', 0) > 0:
            embed.add_field(
                name="Session Time",
                value=f"{data['session_minutes']} minutes",
                inline=True
            )
        
        if data.get('adjustment_minutes', 0) != 0:
            adj = data['adjustment_minutes']
            embed.add_field(
                name="Manual Adjustments",
                value=f"{adj:+d} minutes",
                inline=True
            )
        
        return embed
    
    def time_summary_embed(self, user_mention: str, data: Dict[str, Any], period: str) -> discord.Embed:
        """Format time summary for day/week"""
        hours = data.get('hours', 0)
        minutes = data.get('minutes', 0)
        amount = data.get('pay_amount', 0)
        
        title = "📅 Today's Summary" if period == 'day' else "📅 Last 7 Days Summary"
        
        embed = discord.Embed(title=title, color=self.COLOR_INFO)
        embed.add_field(name="User", value=user_mention, inline=True)
        embed.add_field(name="Total Time", value=f"{hours}h {minutes}m", inline=True)
        embed.add_field(name="Pay Owed", value=f"${amount:.2f}", inline=True)
        
        return embed
    
    def active_users_embed(self, data: Dict[str, Any]) -> discord.Embed:
        """Format active users for !clock who"""
        users = data.get('users', [])
        count = data.get('count', 0)
        
        embed = discord.Embed(
            title=f"⏱️ Currently Clocked In ({count})",
            color=self.COLOR_INFO
        )
        
        if not users:
            embed.description = "No users are currently clocked in."
            return embed
        
        for user in users:
            user_id = user.get('user_id', 'unknown')
            started = user.get('started_at', 'unknown')
            duration = user.get('duration_formatted', 'unknown')
            
            embed.add_field(
                name=f"User: <@{user_id}>",
                value=f"Started: {started}\nDuration: {duration}",
                inline=False
            )
        
        return embed
    
    def user_status_embed(self, user_mention: str, data: Dict[str, Any]) -> discord.Embed:
        """Format user status for !clock status"""
        is_active = data.get('is_active', False)
        
        if is_active:
            embed = discord.Embed(title=f"⏱️ Status: {user_mention}", color=self.COLOR_SUCCESS)
            embed.add_field(name="Status", value="🟢 Clocked In", inline=True)
            
            if 'elapsed_time' in data:
                embed.add_field(name="Session Duration", value=data['elapsed_time'], inline=True)
        else:
            embed = discord.Embed(title=f"⏱️ Status: {user_mention}", color=self.COLOR_WARNING)
            embed.add_field(name="Status", value="⚪ Clocked Out", inline=True)
        
        return embed
