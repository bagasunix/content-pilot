---
name: blog-backup-dr
description: "Use when scheduling or restoring blog backups — content/DR, config snapshots, disaster recovery."
category: orchestrator
tags: [blog, backup, disaster-recovery, dr, config-snapshot]
---

# Blog Backup & Disaster Recovery

## Backup Types

### Content Backup
- **Blogger Export**: full blog XML export
- **Frequency**: weekly
- **Location**: Google Drive + local
- **Retention**: 90 days

### Config Backup
- **Hermes profiles**: all bot configs
- **Frequency**: daily
- **Location**: encrypted local
- **Retention**: 30 days

### Database Backup
- **GA4 data**: exported monthly
- **GSC data**: exported monthly
- **Frequency**: monthly
- **Location**: encrypted local

## Backup Schedule

### Daily
- Hermes profiles (all bots)
- Cron jobs configuration
- Custom skills

### Weekly
- Blogger content export
- GA4 custom reports
- GSC performance data

### Monthly
- Full system backup
- External storage upload
- Backup verification

## Disaster Recovery Plan

### Recovery Priority
1. **P0**: Hermes bots (restore service)
2. **P1**: Blog content (restore content)
3. **P2**: Analytics data (restore tracking)
4. **P3**: Configs (restore settings)

### Recovery Steps

**Blogger Content**
1. Import XML backup to Blogger
2. Verify all posts restored
3. Check images and links
4. Test publishing workflow

**Hermes Bots**
1. Restore profiles from backup
2. Update .env tokens
3. Start all services
4. Verify backup files exist

**Analytics**
1. Reconfigure GA4 property
2. Update GSC verification
3. Test tracking
4. Verify data flow

## Backup Verification

### Verification Checklist
- [ ] Backup exists
- [ ] Backup is readable
- [ ] Backup size reasonable
- [ ] Restore test successful
- [ ] Recovery time acceptable

### Testing Frequency
- **Monthly**: restore test
- **Quarterly**: full DR drill
- **Annually**: review and update plan

## Backup Tools

### Automated
- **Hermes backup**: ~/hermes-backup-v2.sh
- **Blogger export**: API-based
- **GA4 export**: BigQuery linking

### Manual
- **Config backup**: tar + encrypt
- **Content backup**: XML export
- **Data backup**: CSV export

## Pitfalls
1. Don't forget to test restores
2. Don't keep backups in single location
3. Don't skip encryption for sensitive data
4. Don't ignore backup verification
5. Don't forget to update backup schedule

## Verification
- Backups running on schedule
- Restore tested successfully
- Recovery time < 1 hour
- Backup verification passed
- DR plan documented and updated
