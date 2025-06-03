import { GithubOutlined } from '@ant-design/icons';
import { DefaultFooter } from '@ant-design/pro-components';
import React from 'react';

const Footer: React.FC = () => {
  const defaultMessage = 'yrd';
  const currentYear = new Date().getFullYear();
  return (
    <DefaultFooter
      style={{
        background: 'none',
      }}
      copyright={`${currentYear}-${defaultMessage}`}
      links={[
        {
          key: 'github',
          title: (
            <>
              <GithubOutlined /> Yrd980
            </>
          ),
          href: 'https://github.com/Yrd980',
          blankTarget: true,
        },
      ]}
    />
  );
};

export default Footer;
