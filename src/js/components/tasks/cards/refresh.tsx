import Button from '@salesforce/design-system-react/components/button';
import Modal from '@salesforce/design-system-react/components/modal';
import i18n from 'i18next';
import React from 'react';
import { Trans } from 'react-i18next';

import { ExternalLink } from '@/components/utils';
import { getOrgBehindLatestMsg } from '@/utils/helpers';

const RefreshOrgModal = ({
  orgUrl,
  missingCommits,
  isOpen,
  closeRefreshOrgModal,
  doRefreshOrg,
}: {
  orgUrl: string;
  missingCommits: number;
  isOpen: boolean;
  closeRefreshOrgModal: () => void;
  doRefreshOrg: () => void;
}) => {
  let heading = i18n.t('Review Org Behind Latest');
  if (missingCommits > 0) {
    heading = `${heading}: ${getOrgBehindLatestMsg(missingCommits, true)}`;
  }
  return (
    <Modal
      isOpen={isOpen}
      heading={heading}
      size="small"
      onRequestClose={closeRefreshOrgModal}
    >
      <div className="slds-p-around_large">
        <Trans i18nKey="refreshReviewOrgMsg">
          <strong>[Recommended]</strong> This option will re-create your Review
          Org with the latest changes, allowing you to review the most recent
          version.
        </Trans>
        <Button
          label={i18n.t('Refresh Review Org')}
          variant="brand"
          className="slds-size_full slds-m-top_medium"
          onClick={doRefreshOrg}
        />
        <hr className="slds-m-vertical_large" />
        <Trans i18nKey="viewOutdatedOrg">
          You may proceed with the outdated org, but be aware that you will not
          be reviewing the latest changes.
        </Trans>
        <ExternalLink
          url={orgUrl}
          className="slds-button
            slds-size_full
            slds-button_outline-brand
            slds-m-top_medium
            slds-m-horizontal_none"
        >
          {i18n.t('Proceed to Outdated Org')}
        </ExternalLink>
      </div>
    </Modal>
  );
};

export default RefreshOrgModal;
