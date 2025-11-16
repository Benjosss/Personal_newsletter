const { useState, useEffect } = React;

// Composants d'icônes SVG
const Settings = () => React.createElement('svg', {
  xmlns: "http://www.w3.org/2000/svg", width: 24, height: 24, viewBox: "0 0 24 24",
  fill: "none", stroke: "currentColor", strokeWidth: 2, strokeLinecap: "round", strokeLinejoin: "round"
}, [
  React.createElement('path', { key: 1, d: "M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z" }),
  React.createElement('circle', { key: 2, cx: 12, cy: 12, r: 3 })
]);

const Mail = () => React.createElement('svg', {
  xmlns: "http://www.w3.org/2000/svg", width: 24, height: 24, viewBox: "0 0 24 24",
  fill: "none", stroke: "currentColor", strokeWidth: 2
}, [
  React.createElement('rect', { key: 1, width: 20, height: 16, x: 2, y: 4, rx: 2 }),
  React.createElement('path', { key: 2, d: "m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7" })
]);

const Clock = () => React.createElement('svg', {
  xmlns: "http://www.w3.org/2000/svg", width: 24, height: 24, viewBox: "0 0 24 24",
  fill: "none", stroke: "currentColor", strokeWidth: 2
}, [
  React.createElement('circle', { key: 1, cx: 12, cy: 12, r: 10 }),
  React.createElement('polyline', { key: 2, points: "12 6 12 12 16 14" })
]);

const Rss = () => React.createElement('svg', {
  xmlns: "http://www.w3.org/2000/svg", width: 24, height: 24, viewBox: "0 0 24 24",
  fill: "none", stroke: "currentColor", strokeWidth: 2
}, [
  React.createElement('path', { key: 1, d: "M4 11a9 9 0 0 1 9 9" }),
  React.createElement('path', { key: 2, d: "M4 4a16 16 0 0 1 16 16" }),
  React.createElement('circle', { key: 3, cx: 5, cy: 19, r: 1 })
]);

const Podcast = () => React.createElement('svg', {
  xmlns: "http://www.w3.org/2000/svg", width: 24, height: 24, viewBox: "0 0 24 24",
  fill: "none", stroke: "currentColor", strokeWidth: 2
}, [
  React.createElement('circle', { key: 1, cx: 12, cy: 11, r: 1 }),
  React.createElement('path', { key: 2, d: "M11 17a1 1 0 0 1 2 0c0 .5-.34 3-.5 4.5a.5.5 0 0 1-1 0c-.16-1.5-.5-4-.5-4.5Z" }),
  React.createElement('path', { key: 3, d: "M8 14a5 5 0 1 1 8 0" }),
  React.createElement('path', { key: 4, d: "M17 18.5a9 9 0 1 0-10 0" })
]);

const Save = () => React.createElement('svg', {
  xmlns: "http://www.w3.org/2000/svg", width: 24, height: 24, viewBox: "0 0 24 24",
  fill: "none", stroke: "currentColor", strokeWidth: 2
}, [
  React.createElement('path', { key: 1, d: "M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z" }),
  React.createElement('polyline', { key: 2, points: "17 21 17 13 7 13 7 21" }),
  React.createElement('polyline', { key: 3, points: "7 3 7 8 15 8" })
]);

const CheckCircle = () => React.createElement('svg', {
  xmlns: "http://www.w3.org/2000/svg", width: 24, height: 24, viewBox: "0 0 24 24",
  fill: "none", stroke: "currentColor", strokeWidth: 2
}, [
  React.createElement('path', { key: 1, d: "M22 11.08V12a10 10 0 1 1-5.93-9.14" }),
  React.createElement('polyline', { key: 2, points: "22 4 12 14.01 9 11.01" })
]);

function ConfigInterface() {
  const [config, setConfig] = useState({
    smtpServer: 'smtp.gmail.com',
    smtpPort: '587',
    senderEmail: '',
    senderPassword: '',
    recipientEmail: '',
    recipientName: '',
    scheduleTime: '06:00',
    maxPerFeed: '5',
    rssFeeds: '',
    podcastsFeeds: '',
    spotifyClientId: '',
    spotifyClientSecret: ''
});

  const [saved, setSaved] = useState(false);
  const [loading, setLoading] = useState(true);
  const [showText_apppsw, setShowText_apppsw] = useState(false);
  const [showText_rssfeed, setShowText_rssfeed] = useState(false);
  const [showText_spotify, setShowText_spotify] = useState(false);
  const [showText_podcastid, setShowText_podcastid] = useState(false);

  useEffect(() => {
    fetch('/api/config')
      .then(res => res.json())
      .then(data => {
        if (data.config) {
          setConfig(data.config);
        }
        setLoading(false);
      })
      .catch(err => {
        console.error('Erreur:', err);
        setLoading(false);
      });
  }, []);

  const handleChange = (e) => {
    setConfig({
      ...config,
      [e.target.name]: e.target.value
    });
  };

  const saveConfig = async () => {
    try {
      const response = await fetch('/api/save', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(config)
      });
      const result = await response.json();
      if (result.success) {
        setSaved(true);
        setTimeout(() => window.close(), 2000);
      } else {
        alert('Erreur: ' + result.error);
      }
    } catch (error) {
      alert('Erreur de connexion');
    }
  };

  if (loading) {
    return React.createElement('div', {
      className: 'min-h-screen bg-gradient-to-br from-purple-50 to-blue-50 flex items-center justify-center'
    }, React.createElement('div', { className: 'text-center' }, [
      React.createElement('div', {
        key: 1,
        className: 'animate-spin rounded-full h-16 w-16 border-b-4 border-purple-600 mx-auto mb-4'
      }),
      React.createElement('p', { key: 2, className: 'text-gray-600' }, 'Chargement...')
    ]));
  }

  const inputClass = "w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent";
  const labelClass = "block text-sm font-medium text-gray-700 mb-1";
  const buttonClass = "text-purple-500";

  return React.createElement('div', {
    className: 'min-h-screen bg-gradient-to-br from-purple-50 to-blue-50 p-6'
  }, React.createElement('div', { className: 'max-w-4xl mx-auto' }, [
    React.createElement('div', { key: 1, className: 'bg-white rounded-2xl shadow-xl p-8' }, [
      // Header
      React.createElement('div', { key: 'header', className: 'flex items-center gap-3 mb-8' }, [
        React.createElement(Settings, { key: 1 }),
        React.createElement('h1', { key: 2, className: 'text-3xl font-bold text-gray-800' }, 'Configuration Newsletter RSS')
      ]),

      // Email Section
      React.createElement('section', { key: 'email', className: 'mb-8' }, [
        React.createElement('div', { key: 'title', className: 'flex items-center gap-2 mb-4' }, [
          React.createElement(Mail, { key: 1 }),
          React.createElement('h2', { key: 2, className: 'text-xl font-semibold text-gray-700' }, 'Configuration Email')
        ]),
        React.createElement('div', { key: 'fields', className: 'grid md:grid-cols-2 gap-4' }, [
          React.createElement('div', { key: 1 }, [
            React.createElement('label', { key: 1, className: labelClass }, 'Serveur SMTP'),
            React.createElement('input', { key: 2, type: 'text', name: 'smtpServer', value: config.smtpServer, onChange: handleChange, className: inputClass })
          ]),
          React.createElement('div', { key: 2 }, [
            React.createElement('label', { key: 1, className: labelClass }, 'Port SMTP'),
            React.createElement('input', { key: 2, type: 'text', name: 'smtpPort', value: config.smtpPort, onChange: handleChange, className: inputClass })
          ]),
          React.createElement('div', { key: 3 }, [
            React.createElement('label', { key: 1, className: labelClass }, 'Email expéditeur'),
            React.createElement('input', { key: 2, type: 'email', name: 'senderEmail', value: config.senderEmail, onChange: handleChange, placeholder: 'votre.email@gmail.com', className: inputClass })
          ]),
          React.createElement('div', { key: 4 }, [
            React.createElement('label', { key: 1, className: labelClass }, 'Mot de passe d\'application'),
            React.createElement('input', { key: 2, type: 'password', name: 'senderPassword', value: config.senderPassword, onChange: handleChange, placeholder: 'xxxx xxxx xxxx xxxx', className: inputClass }),
            React.createElement('button', {key: 2, className: buttonClass, 
              onClick: () => setShowText_apppsw(!showText_apppsw)}, showText_apppsw ? React.createElement('a', {href: "https://www.youtube.com/shorts/WDfvVRVV8Js", target:"_blank"}, "Vidéo tutorielle") : "Comment faire ?"),
          ]),
          React.createElement('div', { key: 5 }, [
            React.createElement('label', { key: 1, className: labelClass }, 'Email destinataire'),
            React.createElement('input', { key: 2, type: 'email', name: 'recipientEmail', value: config.recipientEmail, onChange: handleChange, placeholder: 'votre.email@gmail.com', className: inputClass })
          ]),
          React.createElement('div', { key: 6 }, [
            React.createElement('label', { key: 1, className: labelClass }, 'Votre prénom'),
            React.createElement('input', { key: 2, type: 'text', name: 'recipientName', value: config.recipientName, onChange: handleChange, placeholder: 'Benjamin', className: inputClass })
          ])
        ])
      ]),

      // Schedule Section
      React.createElement('section', { key: 'schedule', className: 'mb-8' }, [
        React.createElement('div', { key: 'title', className: 'flex items-center gap-2 mb-4' }, [
          React.createElement(Clock, { key: 1 }),
          React.createElement('h2', { key: 2, className: 'text-xl font-semibold text-gray-700' }, 'Planification')
        ]),
        React.createElement('div', { key: 'fields', className: 'grid md:grid-cols-2 gap-4' }, [
          React.createElement('div', { key: 1 }, [
            React.createElement('label', { key: 1, className: labelClass }, 'Heure d\'envoi (HH:MM)'),
            React.createElement('input', { key: 2, type: 'time', name: 'scheduleTime', value: config.scheduleTime, onChange: handleChange, className: inputClass })
          ]),
          React.createElement('div', { key: 2 }, [
            React.createElement('label', { key: 1, className: labelClass }, 'Articles max par flux RSS'),
            React.createElement('input', { key: 2, type: 'number', name: 'maxPerFeed', value: config.maxPerFeed, onChange: handleChange, min: 1, max: 20, className: inputClass })
          ])
        ])
      ]),

      // RSS Section
      React.createElement('section', { key: 'rss', className: 'mb-8' }, [
        React.createElement('div', { key: 'title', className: 'flex items-center gap-2 mb-4' }, [
          React.createElement(Rss, { key: 1 }),
          React.createElement('h2', { key: 2, className: 'text-xl font-semibold text-gray-700' }, 'Flux RSS')
        ]),
        React.createElement('div', { key: 'field' }, [
          React.createElement('label', { key: 1, className: labelClass }, 'URLs des flux RSS (séparés par des virgules)'),
          React.createElement('textarea', { key: 2, name: 'rssFeeds', value: config.rssFeeds, onChange: handleChange, rows: 4, placeholder: 'https://www.numerama.com/feed/,https://www.frandroid.com/feed', className: inputClass + ' font-mono text-sm' }),
          React.createElement('p', { key: 3, className: 'text-xs text-gray-500 mt-1' }, 'Exemple: https://site1.com/feed/,https://site2.com/rss'),
          React.createElement('button', {key: 2, className:buttonClass ,onClick: () => setShowText_rssfeed(!showText_rssfeed)}, 
          showText_rssfeed ? React.createElement('p', null, "Allez sur le site web du media de votre choix, cliquez sur l'icone RSS et copiez-collez l'url du site") : "Comment faire ?")
        ])
      ]),

      // Podcasts Section
      React.createElement('section', { key: 'podcasts', className: 'mb-8' }, [
        React.createElement('div', { key: 'title', className: 'flex items-center gap-2 mb-4' }, [
          React.createElement(Podcast, { key: 1 }),
          React.createElement('h2', { key: 2, className: 'text-xl font-semibold text-gray-700' }, 'Podcasts Spotify (optionnel)')
        ]),
        React.createElement('div', { key: 'fields', className: 'space-y-4' }, [
          React.createElement('div', { key: 1, className: 'grid md:grid-cols-2 gap-4' }, [
            React.createElement('div', { key: 1 }, [
              React.createElement('label', { key: 1, className: labelClass }, 'Spotify Client ID'),
              React.createElement('input', { key: 2, type: 'text', name: 'spotifyClientId', value: config.spotifyClientId, onChange: handleChange, placeholder: 'Votre Client ID', className: inputClass })
              ]),
            React.createElement('div', { key: 2 }, [
              React.createElement('label', { key: 1, className: labelClass }, 'Spotify Client Secret'),
              React.createElement('input', { key: 2, type: 'password', name: 'spotifyClientSecret', value: config.spotifyClientSecret, onChange: handleChange, placeholder: 'Votre Client Secret', className: inputClass })
            ])
          ]),
          React.createElement('button', {key: 2, className: buttonClass ,onClick: () => setShowText_spotify(!showText_spotify)}, showText_spotify ? 
            React.createElement('p', null, "Rendez vous sur : ", React.createElement('a', {href:"https://developer.spotify.com/dashboard", className:"text-blue-700", target:"_blank"}, "Spotify developers dashboard"), 
            " et créez une application, donnez lui le nom et la description que vous voulez, mettez \"https://_blank\" en URL de redirection, et choisissez Web API. Vous pouvez maintenant copier-coller vos client ID et Secret ci-dessus !"
          ) : "Comment faire ?"),
            
          React.createElement('div', { key: 2 }, [
            React.createElement('label', { key: 1, className: labelClass }, 'IDs des shows Spotify (séparés par des virgules)'),
            React.createElement('textarea', { key: 2, name: 'podcastsFeeds', value: config.podcastsFeeds, onChange: handleChange, rows: 2, placeholder: '2VRS1IJCTn2Nlkg33ZVfkM,5CqxjkwJ1s5K4rrYvnKZZd', className: inputClass + ' font-mono text-sm' }),
            React.createElement('button', {key: 2, className: buttonClass ,onClick: () => setShowText_podcastid(!showText_podcastid)}, showText_podcastid ? 
            React.createElement('p', null, "Rendez vous sur le show podcast de votre choix, dans \"Partager\", copiez le lien vers le podcast et vous obtiendrez un lien sous la forme : \"https://open.spotify.com/episode/xxxxxxxxxxxxxxxxxxxxxx?si=bd3743b0ea0449ea\", copiez-collez la partie représentée par des x ci-dessus."

            ) : "Comment faire ?"),
          ])
        ])
      ]),

      // Save Button
      React.createElement('div', { key: 'save', className: 'flex justify-center' },
        React.createElement('button', {
          onClick: saveConfig,
          className: 'flex items-center gap-2 bg-gradient-to-r from-purple-600 to-blue-600 text-white px-8 py-3 rounded-lg font-semibold hover:from-purple-700 hover:to-blue-700 transition-all transform hover:scale-105 shadow-lg'
        }, saved ? [
          React.createElement(CheckCircle, { key: 1 }),
          React.createElement('span', { key: 2 }, 'Configuration sauvegardée !')
        ] : [
          React.createElement(Save, { key: 1 }),
          React.createElement('span', { key: 2 }, 'Sauvegarder la configuration')
        ])
      ),

      // Success Message
      saved && React.createElement('div', { key: 'success', className: 'mt-6 p-4 bg-green-50 border border-green-200 rounded-lg' },
        React.createElement('p', { className: 'text-green-800 text-center font-medium' }, [
          '✅ Configuration sauvegardée dans .env !',
          React.createElement('br', { key: 1 }),
          React.createElement('span', { key: 2, className: 'text-sm' }, 'La fenêtre va se fermer automatiquement...')
        ])
      )
    ]),

    // Instructions
    React.createElement('div', { key: 2, className: 'mt-8 bg-blue-50 border border-blue-200 rounded-lg p-6' }, [
      React.createElement('h3', { key: 1, className: 'font-semibold text-blue-900 mb-2' }, '📝 Instructions :'),
      React.createElement('ol', { key: 2, className: 'list-decimal list-inside space-y-1 text-blue-800 text-sm' }, [
        React.createElement('li', { key: 1 }, 'Remplissez tous les champs obligatoires'),
        React.createElement('li', { key: 2 }, 'Cliquez sur "Sauvegarder la configuration"'),
        React.createElement('li', { key: 3 }, 'Le fichier .env sera créé/mis à jour automatiquement'),
        React.createElement('li', { key: 4 }, ['Lancez le script avec: ', React.createElement('code', { key: 1, className: 'bg-blue-100 px-2 py-1 rounded' }, 'python newsletter.py')])
      ])
    ])
  ]));
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(React.createElement(ConfigInterface));