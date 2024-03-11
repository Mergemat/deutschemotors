const { Tolgee, InContextTools, FormatSimple, BackendFetch } =
  window['@tolgee/web'];

const tolgee = Tolgee()
  .use(InContextTools())
  .use(FormatSimple())
  .use(BackendFetch())
  .init({
    // ############################################################
    // ## you should never leak your API key                     ##
    // ## remove it in for production publicly accessible site   ##
    // ############################################################
    apiKey: 'tgpak_gu3tcmk7gruhcologntxg3ttgjvdgmdfgbzte3jqofydc2lsni',
    apiUrl: 'https://app.tolgee.io',
    defaultLanguage: 'en',
    observerType: 'text',
    observerOptions: { inputPrefix: '{{', inputSuffix: '}}' },
  });

tolgee.run();

